
class Writer():
	def writeMatrix(annotations):
		pass

	def writeVocabularies(vocabularies, location):
		out = open(location+"aaa", "w")
		for x in vocabularies:
			try:
				tmp = "UMLS:{}:T200:Drugs\t".format(x)
				for desc in tsv[x]:
					tmp += desc+"|"
				tmp = tmp[:-1]+"\n"
				out.write(tmp)
			except:
				pass
		out.close()