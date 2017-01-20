import sys
def read_grammar(fname):
	grammar={}
	try:
		with open(fname) as doc:
			for line in doc:
				line=line.split()
				if line[0] in grammar:
					grammar[line[0]].append(line[2:])
				else:
					grammar[line[0]]=[line[2:]]
	except Exception:
		print "Error reading file."
	return grammar

def read_sentence(fname):
	sentences=[]
	try:
		with open(fname) as doc:
			for line in doc:
				line=line.split()
				sentences.append(line[0:])
	except Exception:
		print "Error reading file."

	return sentences

def lookup_word_rule(sentence_word,rules_grammar):
	print ""
	keys_return=[]
	for key in rules_grammar:
		if [sentence_word] in rules_grammar[key]:
			keys_return.append(key)
	return keys_return

def parsing_cky(sentence,rules_grammar):
	chart=[[[] for i in range(len(sentence))] for j in range(len(sentence))]
	for i in range(len(sentence)):
		chart[i][i].extend(lookup_word_rule(sentence[i],rules_grammar))
		row=i-1
		while row>=0:			
			for s in range(row+1,i+1):
				B=[None]
				C=[None]
				B.extend(chart[row][s-1])
				C.extend(chart[s][i])
				if len(B)>1:
					del B[0]
				if len(C)>1:
					del C[0]
				temp_keys=[]
				temp=[[x,y] for x in B for y in C]
				for keys in rules_grammar:
					for item in temp:
						if item in rules_grammar[keys]:
							temp_keys.append(keys)
				if len(temp_keys)>0:
					chart[row][i].extend(temp_keys)
			row-=1
	print "PARSING SENTENCE:",' '.join(sentence)
	print "NUMBER OF PARSERS FOUND:",chart[0][-1].count('S')
	print "CHART:"
	for i,val in enumerate(chart):
		for j,item in enumerate(val):
			if j>=i:
				item.sort()
				if item:
					print "chart[%d][%d]:"%(i+1,j+1),' '.join(item) 
				else:
					print "chart[%d][%d]:"%(i+1,j+1),"-"

def main():
	try:
		rules_grammar=read_grammar(sys.argv[1])
	except Exception:
		rules_grammar=read_grammar("grammar.txt")
	try:
		sentences=read_sentence(sys.argv[2])
	except Exception:
		sentences=read_sentence("sentences.txt")
	for sentence in sentences:
		parsing_cky(sentence,rules_grammar)
main()