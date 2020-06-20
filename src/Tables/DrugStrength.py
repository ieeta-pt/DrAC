from BaseTable import BaseTable
import sqlalchemy as sa

class DrugStrength(BaseTable):
	"""
	Class to build the domain table for uploading automatically the Standard Vocabularies
	"""
	def __init__(self):
		columns = [
			'drug_concept_id',
			'ingredient_concept_id',
			'amount_value',
			'amount_unit_concept_id',
			'numerator_value',
			'numerator_unit_concept_id',
			'denominator_value',
			'denominator_unit_concept_id',
			'box_size',	
			'valid_start_date',
			'valid_end_date',
			'invalid_reason'
		]
		super(Domain, self).__init__(table = "drug_strength")

	def getDataTypesForSQL():
		return {
			'drug_concept_id':				sa.types.Integer,
			'ingredient_concept_id':		sa.types.Integer,
			'amount_value':					sa.types.Float,
			'amount_unit_concept_id':		sa.types.Integer,
			'numerator_value':				sa.types.Float,
			'numerator_unit_concept_id':	sa.types.Integer,
			'denominator_value':			sa.types.Float,
			'denominator_unit_concept_id':	sa.types.Integer,
			'box_size':						sa.types.Integer,
			'valid_start_date':				sa.types.Date,
			'valid_end_date':				sa.types.Date,
			'invalid_reason':				sa.types.String
		}
   