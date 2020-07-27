
class Harmonizer():
	def harmonize(matrix, usagiOutput):
		"""
		This method harmonizes the concepts in the matrix to their standard defition.
		These mappings were validated in the Usagi tool and here that output is used.
		:param matrix:
		:param usagiOuput:
		:return:
		"""
		headers = Harmonizer._harmonizeHeaders(matrix[0], usagiOutput)
		data = matrix[1:]

		return None

	def _harmonizeHeaders(headers, usagiOutput):
		stdHeaders = []
		return stdHeaders

	def migrate():
		return None
	

#return pd.DataFrame(outputDataDict, columns = dfRead.columns.values)