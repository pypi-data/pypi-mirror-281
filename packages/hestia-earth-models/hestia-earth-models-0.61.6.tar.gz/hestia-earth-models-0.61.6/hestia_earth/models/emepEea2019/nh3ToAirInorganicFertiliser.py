from functools import reduce
from hestia_earth.schema import EmissionMethodTier
from hestia_earth.utils.lookup import download_lookup
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils import _filter_list_term_unit
from hestia_earth.models.utils.completeness import _is_term_type_complete
from hestia_earth.models.utils.inorganicFertiliser import (
    get_NH3_emission_factor, get_terms, get_term_lookup, BREAKDOWN_LOOKUP, get_country_breakdown, get_cycle_inputs
)
from hestia_earth.models.utils.constant import Units
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.measurement import most_relevant_measurement_value
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "completeness.fertiliser": "True",
        "inputs": [
            {
                "@type": "Input",
                "value": "",
                "term.termType": "inorganicFertiliser",
                "optional": {
                    "properties": [{"@type": "Property", "value": "", "term.@id": "nitrogenContent"}]
                }
            },
            {
                "@type": "Input",
                "value": "",
                "term.termType": "fertiliserBrandName",
                "properties": [{"@type": "Property", "value": "", "key.termType": "inorganicFertiliser"}]
            }
        ],
        "site": {
            "@type": "Site",
            "country": {"@type": "Term", "termType": "region"},
            "measurements": [
                {"@type": "Measurement", "value": "", "term.@id": "soilPh"},
                {"@type": "Measurement", "value": "", "term.@id": "temperatureAnnual"}
            ]
        }
    }
}
LOOKUPS = {
    "inorganicFertiliser": ["NH3_emissions_factor_acidic", "NH3_emissions_factor_basic"],
    "region-inorganicFertiliser-fertGroupingNitrogen-breakdown": ""
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "tier 2"
    }]
}
TERM_ID = 'nh3ToAirInorganicFertiliser'
TIER = EmissionMethodTier.TIER_2.value
UNSPECIFIED_TERM_ID = 'inorganicNitrogenFertiliserUnspecifiedKgN'


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    return emission


def _get_input_value(cycle: dict, soilPh: float, temperature: float):
    def get_value(input: dict):
        term_id = input.get('term', {}).get('@id')
        factor = get_NH3_emission_factor(term_id, soilPh, temperature)
        value = list_sum(input.get('value'))
        debugValues(cycle, model=MODEL, term=TERM_ID,
                    product=term_id,
                    factor=factor,
                    value=value)
        return value * factor
    return get_value


def _run(cycle: dict, temperature: float, soilPh: float, inputs: float):
    return list_sum(list(map(_get_input_value(cycle, soilPh, temperature), inputs)))


def _get_groupings():
    term_ids = get_terms()

    def get_grouping(groupings: dict, term_id: str):
        grouping = get_term_lookup(term_id, 'fertGroupingNitrogen')
        return {**groupings, **({grouping: term_id} if len(grouping) > 0 else {})}

    return reduce(get_grouping, term_ids, {})


def _get_term_value(cycle: dict, soilPh: float, temperature: float, country_id: str, grouping: str, term_id: str):
    factor = get_NH3_emission_factor(term_id, soilPh, temperature)
    value = get_country_breakdown(MODEL, TERM_ID, country_id, grouping)
    debugValues(cycle, model=MODEL, term=TERM_ID,
                grouping=grouping,
                NH3_factor=factor,
                country_breakdown=value)
    return value * factor


def _run_with_unspecified(cycle: dict, temperature: float, soilPh: float, unspecifiedKgN_value: float, country_id: str):
    # creates a dictionary grouping => term_id with only a single key per group (avoid counting twice)
    groupings = _get_groupings()
    return list_sum([
        _get_term_value(cycle, soilPh, temperature, country_id, grouping, term_id)
        for grouping, term_id in groupings.items()
    ]) * unspecifiedKgN_value


def _should_run(cycle: dict):
    end_date = cycle.get('endDate')
    site = cycle.get('site', {})
    measurements = site.get('measurements', [])
    soilPh = most_relevant_measurement_value(measurements, 'soilPh', end_date)
    temperature = most_relevant_measurement_value(
        measurements, 'temperatureAnnual', end_date) or most_relevant_measurement_value(
        measurements, 'temperatureLongTermAnnualMean', end_date)

    inputs = get_cycle_inputs(cycle)
    N_inputs = _filter_list_term_unit(inputs, Units.KG_N)
    has_N_inputs = len(N_inputs) > 0

    unspecifiedKgN = find_term_match(cycle.get('inputs', []), UNSPECIFIED_TERM_ID).get('value', [])
    fertiliser_complete = _is_term_type_complete(cycle, 'fertiliser')
    has_unspecifiedKgN = len(unspecifiedKgN) > 0 or fertiliser_complete

    country_id = site.get('country', {}).get('@id')
    lookup = download_lookup(BREAKDOWN_LOOKUP)
    has_country_data = country_id in list(lookup.termid)

    run_with_unspecified = (has_country_data and has_unspecifiedKgN) or fertiliser_complete
    unspecifiedKgN = (
        0 if len(unspecifiedKgN) == 0 and fertiliser_complete else list_sum(unspecifiedKgN, None)
    ) if run_with_unspecified else None

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    temperature=temperature,
                    soilPh=soilPh,
                    term_type_fertiliser_complete=fertiliser_complete,
                    has_unspecifiedKgN=has_unspecifiedKgN,
                    has_country_data=has_country_data,
                    run_with_unspecified=run_with_unspecified,
                    has_N_inputs=has_N_inputs)

    should_run = all([
        temperature,
        soilPh,
        any([
            run_with_unspecified,
            has_N_inputs,
            not has_N_inputs and fertiliser_complete
        ])
    ])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, temperature, soilPh, N_inputs, unspecifiedKgN, country_id


def run(cycle: dict):
    should_run, temperature, soilPh, N_inputs, unspecifiedKgN, country_id = _should_run(cycle)
    value = _run(cycle, temperature, soilPh, N_inputs) or (
        _run_with_unspecified(cycle, temperature, soilPh, unspecifiedKgN, country_id)
        if unspecifiedKgN is not None else None
    ) if should_run else None
    return [_emission(value)] if value is not None else []
