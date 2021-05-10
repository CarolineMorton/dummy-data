######################################

# Some covariates used in the study are created from codelists of clinical conditions or
# numerical values available on a patient's records.
# This script fetches all of the codelists identified in codelists.txt from OpenCodelists.

######################################


# --- IMPORT STATEMENTS ---

## Import code building blocks from cohort extractor package
from cohortextractor import (codelist, codelist_from_csv, combine_codelists)


## Ethnicity
ethnicity_codes = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-eth2001.csv",
    system="snomed",
    column="code",
    category_column="grouping_16_id",
)

## BMI
bmi_codes = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-bmi.csv",
    system = "snomed",
    column = "code",
)

## Diabetes
diabetes_codes = codelist_from_csv(
  "codelists/primis-covid19-vacc-uptake-diab.csv",
  system = "snomed",
  column = "code",
)

## Chronic Liver disease codes
chronis_liver_disease_codes = codelist_from_csv(
  "codelists/primis-covid19-vacc-uptake-cld.csv",
  system = "snomed",
  column = "code",
)

covid_primary_care_code = codelist_from_csv(
  "codelists/user-will-hulme-covid-identification-in-primary-care-probable-covid-clinical-code.csv",
  system = "snomed",
  column = "code",
)

covid_primary_care_positive_test = codelist_from_csv(
  "codelists/user-will-hulme-covid-identification-in-primary-care-probable-covid-positive-test.csv",
  system = "snomed",
  column = "code",
)

covid_primary_care_sequalae = codelist_from_csv(
  "codelists/user-will-hulme-covid-identification-in-primary-care-probable-covid-sequelae.csv",
  system = "snomed",
  column = "code",
)