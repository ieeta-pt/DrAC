import sqlalchemy as sa

class Person(BaseTable):
    def __init__(self):
        columns = [
            'person_id',
            'gender_concept_id',
            'year_of_birth',
            'month_of_birth',
            'day_of_birth',
    		'birth_datetime',
            'death_datetime',
            'race_concept_id',
            'ethnicity_concept_id',
            'location_id',
    		'provider_id',
            'care_site_id',
            'person_source_value',
            'gender_source_value',
            'gender_source_concept_id',
    		'race_source_value',
            'race_source_concept_id',
            'ethnicity_source_value',
            'ethnicity_source_concept_id'
        ]

    def getDataTypesForSQL():
        return {
            'person_id':                    sa.types.BigInteger,
            'gender_concept_id':            sa.types.BigInteger,
            'year_of_birth':                sa.types.Integer,
            'month_of_birth':               sa.types.Integer,
            'day_of_birth':                 sa.types.Integer,
            'birth_datetime':               sa.types.String,
            'death_datetime':               sa.types.String,
            'race_concept_id':              sa.types.BigInteger,
            'ethnicity_concept_id':         sa.types.BigInteger,
            'location_id':                  sa.types.BigInteger,
            'provider_id':                  sa.types.BigInteger,
            'care_site_id':                 sa.types.BigInteger,
            'person_source_value':          sa.types.String,
            'gender_source_value':          sa.types.String,
            'gender_source_concept_id':     sa.types.BigInteger,
            'race_source_value':            sa.types.String,
            'race_source_concept_id':       sa.types.BigInteger,
            'ethnicity_source_value':       sa.types.String,
            'ethnicity_source_concept_id':  sa.types.BigInteger 
        }