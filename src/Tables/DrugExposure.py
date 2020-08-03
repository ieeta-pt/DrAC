#from BaseTable import BaseTable
import sqlalchemy as sa

class DrugExposure():#BaseTable):
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

	def __init__(self, 
				drug_exposure_id,
				person_id,
				drug_concept_id,
				drug_exposure_start_datetime,
				drug_type_concept_id,
				route_concept_id,
				drug_source_concept_id,
				drug_exposure_start_date = "",
				drug_exposure_end_date = "",
				drug_exposure_end_datetime = "",
				verbatim_end_date = "",
				stop_reason = "",
				refills = "",
				quantity = "",
				days_supply = "",
				sig = "",
				lot_number = "",
				provider_id = "",
				visit_occurrence_id = "",
				visit_detail_id = "",
				drug_source_value = "",
				route_source_value = "",
				dose_unit_source_value = ""):
		self.drug_exposure_id = drug_exposure_id
		self.person_id = person_id
		self.drug_concept_id = drug_concept_id
		self.drug_exposure_start_date = drug_exposure_start_date
		self.drug_exposure_start_datetime = drug_exposure_start_datetime
		self.drug_exposure_end_date = drug_exposure_end_date
		self.drug_exposure_end_datetime = drug_exposure_end_datetime
		self.verbatim_end_date = verbatim_end_date
		self.drug_type_concept_id = drug_type_concept_id
		self.stop_reason = stop_reason
		self.refills = refills
		self.quantity = quantity
		self.days_supply = days_supply
		self.sig = sig
		self.route_concept_id = route_concept_id
		self.lot_number = lot_number
		self.provider_id = provider_id
		self.visit_occurrence_id = visit_occurrence_id
		self.visit_detail_id = visit_detail_id
		self.drug_source_value = drug_source_value
		self.drug_source_concept_id = drug_source_concept_id
		self.route_source_value = route_source_value
		self.dose_unit_source_value = dose_unit_source_value
		
	def getRow(self):
		return  str(self.drug_exposure_id) + \
				"\t" + str(self.person_id) + \
				"\t" + self.drug_concept_id + \
				"\t" + self.drug_exposure_start_date + \
				"\t" + self.drug_exposure_start_datetime + \
				"\t" + self.drug_exposure_end_date + \
				"\t" + self.drug_exposure_end_datetime + \
				"\t" + self.verbatim_end_date + \
				"\t" + self.drug_type_concept_id + \
				"\t" + self.stop_reason + \
				"\t" + self.refills + \
				"\t" + self.quantity + \
				"\t" + self.days_supply + \
				"\t" + self.sig + \
				"\t" + self.route_concept_id + \
				"\t" + self.lot_number + \
				"\t" + self.provider_id + \
				"\t" + self.visit_occurrence_id + \
				"\t" + self.visit_detail_id + \
				"\t" + self.drug_source_value + \
				"\t" + self.drug_source_concept_id + \
				"\t" + self.route_source_value + \
				"\t" + self.dose_unit_source_value

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
