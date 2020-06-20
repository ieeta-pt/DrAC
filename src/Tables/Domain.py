from BaseTable import BaseTable
import sqlalchemy as sa

class Domain(BaseTable):
	"""
	Class to build the domain table for uploading automatically the Standard Vocabularies
	"""
	def __init__(self):
		columns = [
			'domain_id',
			'domain_name',
			'domain_concept_id'
		]
		super(Domain, self).__init__(table = "domain")

	def getDataTypesForSQL():
		return {
			'domain_id':         sa.types.String,
			'domain_name':       sa.types.String,
			'domain_concept_id': sa.types.BigInteger
		}
   