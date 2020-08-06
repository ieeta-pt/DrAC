#from BaseTable import BaseTable
from Tables.BaseTable import BaseTable
import sqlalchemy as sa

class Note(BaseTable):
	columns = [
		'note_id',
		'person_id',
		'note_event_id',
		'note_event_field_concept_id',
		'note_date',
		'note_datetime',
		'note_type_concept_id',
		'note_class_concept_id',
		'note_title',
		'note_text',
		'encoding_concept_id',
		'language_concept_id',
		'provider_id',
		'visit_occurrence_id',
		'visit_detail_id',
		'note_source_value'
	]
	def __init__(self,
				note_id,
				person_id,
				note_text,
				note_datetime,
				encoding_concept_id,
				language_concept_id,
				note_type_concept_id,
				note_class_concept_id,
				note_event_id = "",
				note_event_field_concept_id = "",
				note_date = "",
				note_title = "",
				provider_id = "",
				visit_occurrence_id = "",
				visit_detail_id = "",
				note_source_value = ""):
		super(Note, self).__init__(table = "note")
		self.note_id = note_id
		self.person_id = person_id
		self.note_text = note_text
		self.note_datetime = note_datetime
		self.encoding_concept_id = encoding_concept_id
		self.language_concept_id = language_concept_id
		self.note_event_id = note_event_id
		self.note_event_field_concept_id = note_event_field_concept_id
		self.note_date = note_date
		self.note_type_concept_id = note_type_concept_id
		self.note_class_concept_id = note_class_concept_id
		self.note_title = note_title
		self.provider_id = provider_id
		self.visit_occurrence_id = visit_occurrence_id
		self.visit_detail_id = visit_detail_id
		self.note_source_value = note_source_value

	def getRow(self):
		return 	str(self.note_id) + "\t" + \
	 			str(self.person_id) + "\t" + \
	 			self.note_event_id + "\t" + \
	 			self.note_event_field_concept_id + "\t" + \
	 			self.note_date + "\t" + \
	 			self.note_datetime + "\t" + \
	 			self.note_type_concept_id + "\t" + \
	 			self.note_class_concept_id + "\t" + \
	 			self.note_title + "\t" + \
	 			self.note_text + "\t" + \
	 			self.encoding_concept_id + "\t" + \
	 			self.language_concept_id + "\t" + \
	 			self.provider_id + "\t" + \
	 			self.visit_occurrence_id + "\t" + \
	 			self.visit_detail_id + "\t" + \
	 			self.note_source_value

	def getDataTypesForSQL():
		return {
 			'note_id':						sa.types.BigInteger,
 			'person_id':					sa.types.BigInteger,
 			'note_event_id':				sa.types.BigInteger,
 			'note_event_field_concept_id':	sa.types.Integer,
 			'note_date':					sa.types.Date,
 			'note_datetime':				sa.types.String,
 			'note_type_concept_id':			sa.types.Integer,
 			'note_class_concept_id':		sa.types.Integer,
 			'note_title':					sa.types.String,
 			'note_text':					sa.types.String,
 			'encoding_concept_id':			sa.types.Integer,
 			'language_concept_id':			sa.types.Integer,
 			'provider_id':					sa.types.BigInteger,
 			'visit_occurrence_id':			sa.types.BigInteger,
 			'visit_detail_id':				sa.types.BigInteger,
 			'note_source_value':			sa.types.String
		}