from BaseTable import BaseTable
import sqlalchemy as sa

class Relationship(BaseTable):
	"""
	Class to build the relationship table for uploading automatically the Standard Vocabularies
	"""
	def __init__(self, content):
		columns = [
			'relationship_id',
			'relationship_name',
			'is_hierarchical',
			'defines_ancestry',
			'reverse_relationship_id',
			'relationship_concept_id'
		]
		super(Relationship, self).__init__(table = "relationship")

	def getDataTypesForSQL():
		return {
			'relationship_id':			sa.types.String,
			'relationship_name':		sa.types.String,
			'is_hierarchical':			sa.types.String,
			'defines_ancestry':			sa.types.String,
			'reverse_relationship_id':	sa.types.String,
			'relationship_concept_id':	sa.types.BigInteger
		}
   