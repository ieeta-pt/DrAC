from BaseTable import BaseTable
import sqlalchemy as sa

class ConceptAncestor(BaseTable):
	"""
	Class to build the concept_ancestor table for uploading automatically the Standard Vocabularies
	"""
	def __init__(self):
		columns = [
			'ancestor_concept_id',
			'descendant_concept_id',
			'min_levels_of_separation',
			'max_levels_of_separation'
		]
		super(ConceptAncestor, self).__init__(table = "concept_ancestor")

	def getDataTypesForSQL():
		return {
			'ancestor_concept_id':		sa.types.BigInteger,
			'descendant_concept_id':	sa.types.BigInteger,
			'min_levels_of_separation': sa.types.BigInteger,
			'max_levels_of_separation': sa.types.BigInteger
		}
	 