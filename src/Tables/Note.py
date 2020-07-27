import sqlalchemy as sa

class Note(BaseTable):
	def __init__(self):
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