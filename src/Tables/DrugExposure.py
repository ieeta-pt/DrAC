import sqlalchemy as sa

class DrugExposure(BaseTable):
	def __init__(self):
		columns = [
			'drug_exposure_id',
			'person_id',
			'drug_concept_id',
			'drug_exposure_start_date',
			'drug_exposure_start_datetime',
			'drug_exposure_end_date',
			'drug_exposure_end_datetime',
			'verbatim_end_date',
			'drug_type_concept_id',
			'stop_reason',
			'refills',
			'quantity',
			'days_supply',
			'sig',
			'route_concept_id',
			'lot_number',
			'provider_id',
			'visit_occurrence_id',
			'visit_detail_id',
			'drug_source_value',
			'drug_source_concept_id',
			'route_source_value',
			'dose_unit_source_value',
		]
		

	def getDataTypesForSQL():
		return {
			'drug_exposure_id':              sa.types.BigInteger,
			'person_id':                     sa.types.BigInteger,
			'drug_concept_id':               sa.types.BigInteger,
			'drug_exposure_start_date':      sa.types.Date,
			'drug_exposure_start_datetime':  sa.types.String,
			'drug_exposure_end_date':        sa.types.Date,
			'drug_exposure_end_datetime':    sa.types.String,
			'verbatim_end_date':             sa.types.Date,
			'drug_type_concept_id':          sa.types.BigInteger,
			'stop_reason':                   sa.types.String,
			'refills':                       sa.types.BigInteger,
			'quantity':                      sa.types.Float,
			'days_supply':                   sa.types.BigInteger,
			'sig':                           sa.types.String,
			'route_concept_id':	             sa.types.BigInteger,
			'lot_number':                    sa.types.String,
			'provider_id':                   sa.types.BigInteger,
			'visit_occurrence_id':		     sa.types.BigInteger,
			'visit_detail_id':		         sa.types.BigInteger,
			'drug_source_value':             sa.types.String,
			'drug_source_concept_id':        sa.types.BigInteger,
			'route_source_value':            sa.types.String,
			'dose_unit_source_value':        sa.types.String
		}
