#from BaseTable import BaseTable
from Tables.BaseTable import BaseTable
import sqlalchemy as sa

class NoteNLP(BaseTable):
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

	def __init__(self,
				note_nlp_id,
				note_id,
				nlp_date,
				section_concept_id,
				lexical_variant,
				note_nlp_concept_id,
				note_nlp_source_concept_id,
				snippet = "",
				offset = "",
				nlp_system = "",
				nlp_datetime = "",
				term_exists = "",
				term_temporal = "",
				term_modifiers = ""):
		super(NoteNLP, self).__init__(table = "note_nlp")
		self.note_nlp_id = note_nlp_id
		self.note_id = note_id
		self.nlp_date = nlp_date
		self.section_concept_id = section_concept_id
		self.lexical_variant = lexical_variant
		self.note_nlp_concept_id = note_nlp_concept_id
		self.note_nlp_source_concept_id = note_nlp_source_concept_id
		self.snippet = snippet
		self.offset = offset
		self.nlp_system = nlp_system
		self.nlp_datetime = nlp_datetime
		self.term_exists = term_exists
		self.term_temporal = term_temporal
		self.term_modifiers = term_modifiers

	def getRow(self):
		return 	str(self.note_nlp_id) + "\t" + \
				str(self.note_id) + "\t" + \
				str(self.section_concept_id) + "\t" + \
				self.snippet + "\t" + \
				self.offset + "\t" + \
				self.lexical_variant + "\t" + \
				self.note_nlp_concept_id + "\t" + \
				self.nlp_system + "\t" + \
				self.nlp_date + "\t" + \
				self.nlp_datetime + "\t" + \
				self.term_exists + "\t" + \
				self.term_temporal + "\t" + \
				self.term_modifiers + "\t" + \
				self.note_nlp_source_concept_id

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