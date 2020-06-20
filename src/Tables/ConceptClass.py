from BaseTable import BaseTable
import sqlalchemy as sa

class ConceptClass(BaseTable):
	"""
	Class to build the concept_class table for uploading automatically the Standard Vocabularies
	"""
	def __init__(self, content):
		columns = [
			'concept_class_id',
			'concept_class_name',
			'concept_class_concept_id'
		]
		super(ConceptClass, self).__init__(table = "concept_class")

	def getDataTypesForSQL():
		return {
			'concept_class_id':			sa.types.String,
			'concept_class_name':		sa.types.String,
			'concept_class_concept_id':	sa.types.BigInteger
		}
   