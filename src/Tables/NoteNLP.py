import sqlalchemy as sa

class NoteNLP(BaseTable):
	def __init__(self):
		columns = [
			'note_nlp_id',
			'note_id',
			'section_concept_id',
			'snippet',
			'"offset"',
			'lexical_variant',
			'note_nlp_concept_id',
			'nlp_system',
			'nlp_date',
			'nlp_datetime',
			'term_exists',
			'term_temporal',
			'term_modifiers',
			'note_nlp_source_concept_id'
		]

	def getDataTypesForSQL():
		return {
			'note_nlp_id':					sa.types.BigInteger,
			'note_id':						sa.types.BigInteger,
			'section_concept_id':			sa.types.Integer,
			'snippet':						sa.types.String,
			'"offset"':					    sa.types.String,
			'lexical_variant':				sa.types.String,
			'note_nlp_concept_id':			sa.types.Integer,
			'nlp_system':					sa.types.String,
			'nlp_date':						sa.types.Date,
			'nlp_datetime':					sa.types.String,
			'term_exists':					sa.types.String,
			'term_temporal':				sa.types.String,
			'term_modifiers':				sa.types.String,
			'note_nlp_source_concept_id':  	sa.types.Integer
		}