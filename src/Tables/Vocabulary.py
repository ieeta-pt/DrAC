from BaseTable import BaseTable
import sqlalchemy as sa

class Vocabulary(BaseTable):
	"""
	Class to build the vocabulary table for uploading automatically the Standard Vocabularies
	"""
	def __init__(self):
		columns = [
			'vocabulary_id',
			'vocabulary_name',
			'vocabulary_reference',
			'vocabulary_version',
			'vocabulary_concept_id'
		]
		super(Vocabulary, self).__init__(table = "vocabulary")

	def getDataTypesForSQL():
		return {
			'vocabulary_id':			sa.types.String,
			'vocabulary_name':			sa.types.String,
			'vocabulary_reference':		sa.types.String,
			'vocabulary_version':		sa.types.String,
			'vocabulary_concept_id':	sa.types.BigInteger
		}
   