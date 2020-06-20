from BaseTable import BaseTable
import sqlalchemy as sa

class ConceptSynonym(BaseTable):
	"""
	Class to build the concept_synonym table for uploading automatically the Standard Vocabularies
	"""
	def __init__(self, content):
		columns = [
			'concept_id',
			'concept_synonym_name',
			'language_concept_id'
		]
		super(ConceptSynonym, self).__init__(table = "concept_synonym")

	def getDataTypesForSQL():
		return {
			'concept_id':            sa.types.BigInteger,
			'concept_synonym_name':  sa.types.String,
			'language_concept_id':   sa.types.BigInteger
		}
   