from BaseTable import BaseTable
import sqlalchemy as sa

class ConceptRelationship(BaseTable):
	"""
	Class to build the concept_relationship table for uploading automatically the Standard Vocabularies
	"""
	def __init__(self, content):
		columns = [
			'concept_id_1',
			'concept_id_2',
			'relationship_id',
			'valid_start_date',
			'valid_end_date',
			'invalid_reason'
		]
		super(ConceptRelationship, self).__init__(table = "concept_relationship")

	def getDataTypesForSQL():
		return {
			'concept_id_1':		sa.types.BigInteger,
			'concept_id_2':		sa.types.BigInteger,
			'relationship_id':	sa.types.String,
			'valid_start_date':	sa.types.String,
			'valid_end_date':	sa.types.Date,
			'invalid_reason':	sa.types.String
		}
   