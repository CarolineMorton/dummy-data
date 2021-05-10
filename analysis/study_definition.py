from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv

## Import codelists from codelist.py (which pulls them from the codelist folder)
from codelists import *


study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.registered_with_one_practice_between(
        "2019-02-01", "2020-02-01"
    ),

    # Set index date to start date
    index_date = "2020-02-01",

    ## DEMOGRAPHIC INFORMATION
    ### Age
    age=patients.age_as_of(
        "2020-03-31",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
            "incidence": 0.001
        },
    ),

    ### Sex
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),

    ### Ethnicity
    ethnicity=patients.with_these_clinical_events(
        ethnicity_codes,
        returning="category",
        find_last_match_in_period=True,
        on_or_before="index_date",
        return_expectations={
            "category": {
                "ratios": {
                    "1": 0.25,
                    "2": 0.05,
                    "3": 0.05,
                    "4": 0.05,
                    "5": 0.05,
                    "6": 0.05,
                    "7": 0.05,
                    "8": 0.05,
                    "9": 0.05,
                    "10": 0.05,
                    "11": 0.05,
                    "12": 0.05,
                    "13": 0.05,
                    "14": 0.05,
                    "15": 0.05,
                    "16": 0.05,
                }
            },
            "incidence": 0.75,
        },
    ),
    ### BMI
    bmi=patients.with_these_clinical_events(
        bmi_codes,
        returning="numeric_value",
        ignore_missing_values=True,
        find_last_match_in_period=True,
        on_or_before="index_date",
        return_expectations={
            "float": {"distribution": "normal", "mean": 28, "stddev": 5},
        },
    ),

    ### Diabetes
    diabetes=patients.with_these_clinical_events(
        diabetes_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        on_or_before="index_date",
        return_expectations={"incidence": 0.10},
    ),

    ### Chronic liver disease
      chronic_liver_disease = patients.with_these_clinical_events(
        chronis_liver_disease_codes,
        on_or_before = "index_date",
        returning = "binary_flag",
        return_expectations = {"incidence": 0.01},
      ),

    ### Index of multiple deprivation
    imd=patients.categorised_as(
        {"0": "DEFAULT",
         "1": """index_of_multiple_deprivation >=1 AND index_of_multiple_deprivation < 32844*1/5""",
         "2": """index_of_multiple_deprivation >= 32844*1/5 AND index_of_multiple_deprivation < 32844*2/5""",
         "3": """index_of_multiple_deprivation >= 32844*2/5 AND index_of_multiple_deprivation < 32844*3/5""",
         "4": """index_of_multiple_deprivation >= 32844*3/5 AND index_of_multiple_deprivation < 32844*4/5""",
         "5": """index_of_multiple_deprivation >= 32844*4/5 """,
         },
        index_of_multiple_deprivation=patients.address_as_of(
            "index_date",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.01,
                    "1": 0.20,
                    "2": 0.20,
                    "3": 0.20,
                    "4": 0.20,
                    "5": 0.19,
                }},
        }
    ),
    ### Region - NHS England 9 regions
    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and The Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East": 0.1,
                    "London": 0.2,
                    "South West": 0.1,
                    "South East": 0.1, }, },
        },
    ),

    ### STP (regional grouping of practices)
    stp=patients.registered_practice_as_of("index_date",
                                           returning="stp_code",
                                           return_expectations={
                                               "rate": "universal",
                                               "category": {
                                                   "ratios": {
                                                       "STP1": 0.1,
                                                       "STP2": 0.1,
                                                       "STP3": 0.1,
                                                       "STP4": 0.1,
                                                       "STP5": 0.1,
                                                       "STP6": 0.1,
                                                       "STP7": 0.1,
                                                       "STP8": 0.1,
                                                       "STP9": 0.1,
                                                       "STP10": 0.1, }},
                                           },
                                           ),

    ### Urban vs rural
    rural_urban=patients.address_as_of(
        "index_date",
        returning="rural_urban_classification",
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {
                1: 0.125,
                2: 0.125,
                3: 0.125,
                4: 0.125,
                5: 0.125,
                6: 0.125,
                7: 0.125,
                8: 0.125}
            },
        },
    ),

    ### History of covid
    prior_covid_date=patients.with_these_clinical_events(
        combine_codelists(
            covid_primary_care_code,
            covid_primary_care_positive_test,
            covid_primary_care_sequalae,
        ),
        returning="date",
        date_format="YYYY-MM-DD",
        on_or_before="index_date",
        find_first_match_in_period=True,
        return_expectations={"rate": "exponential_increase"},
    ),
)

