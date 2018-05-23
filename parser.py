#Petros Skordas
#AM P2015070
#project2 Compilers

import plex

#A user defined exception class, to describe parse errors.
class ParseError(Exception):	
	pass

#The class encapsulating all parsing functionality for this grammar
class MyParser:

	#Creating a plex scanner for this grammar
	def create_scanner(self,fp):

		#Define some pattern constructs here
		boolean_true = plex.NoCase(plex.Str("true","t","1")
		boolean_false = plex.NoCase(plex.Str("false","f","1")

		parenethesis = plex.Str("(",")")
		equals = plex.Str("=")		

		not_operator = plex.Str("NOT")
		and_operator = plex.Str("AND")
		or_operator = plex.Str("OR")

		space = plex.Any(" \t\n")
		letter = plex.Range("azAZ")
		digit = plex.Range("09")
		name = letter + plex.Rep(letter | digit)
		keyword = plex.Str("print") 

		#The scanner lexicon
		lexicon = plex.Lexicon([
			(boolean_true,"TRUE"),
			(boolean_false,"FALSE"),
			(parenthesis,plex.TEXT),
			(equals,"="),
			(not_operator,"NOT"),
			(and_operator,"AND"),
			(or_operator<"OR"),
			(keyword,"print"),
			(space,plex.IGNORE),
			(name,"identifier")
			])
	
		#Creating and storing the scanner object
		self.scanner = plex.Scanner(lexicon,fp)

		#Get initial lookahead
		self.la,self.val = self.next_token()

	#Returns next token, matched text
	def next_token(self):
		return self.scanner.read()

	#Returns position in case of errors
	def position(self):
		return self.scanner.position()

	#Consumes an expected token. Raises parse error if anything else is found
	def match(self,token):
		if self.la==token:
			self.la,self.val = self.next_token()
		else:
			raise ParseError("found {} instead of {}".format(self.la,token))

	#Creates scanner for input file object fp and calls the parse logic code
	def parse(self,fp):
		self.create_scanner(fp)
		self.stmt_List()

	#LL(1) grammar here
	#Stmt_list -> Stmt Stmt_list | ε
	def stmt_list(self):
		if self.la == "identifier" or self.la == "print":
			self.stmt()
			self.stmt_list()
		elif self.la is None:
			return
		else:
			raise ParseError("Expected id or print ")
	#Stmt -> id = Expr | print Expr
	def stmt(self):
		if self.la == "identifier":
			self.match("identifier")
			self.match("=")
			self.expr()
		elif self.la == "print":
			self.match("print")
			self.expr()
		else:
			raise ParseError("Expected id or print ")
	#Expr -> Term Term_tail
	def expr(self):
		if self.la == "(" or self.la == "identifier" or self.la == "TRUE" or self.la == "FALSE" or self.la == "NOT":
			self.term()
			self.term_tail()
		else:
			raise ParseError("Expected id or true or false")

	#Term_tail -> OR Term Term_tail
	def term_tail(self):
		if self.la == "OR":
			self.or_operator()
			self.term()
			self.term_tail()
		elif self.la == ")" or self.la == "identifier" or self.la == "print":
			return
		elif self.la is None:
			return
		else:
			raise ParseError("Expected AND")

	#Term -> Term Term_tail
	def term(self):
		if self.la == "(" or self.la == "identifier" or self.la == "TRUE" or self.la == "FALSE":
			self.factor()
			self.factor_tail()
		else:
			raise ParseError("Expected identifier or boolean")

	#Factor_tail ->
	def factor_tail(self):
		if self.la == "AND":
			self.and_operator()
			self.factor()
			self.factor_tail()
		elif self.la == ")" or self.la == "OR" or self.la == "identifier" or self.la == "print":
			return
		elif self.la is None:
			return
		else:
			raise ParseError("Expected NOT")
	
	#Factor ->
	def factor(self):
		if self.la == "(" or self.la == "identifier" or self.la == "TRUE" or self.la == "FALSE":
			self.not_operator()
			self.fnot_operator()
		else:
			raise ParseError("Expected ( or id or boolean")
	
	#fnot_operator ->
	def fnot_operator(self):
		if self.la == "(":
			self.match("(")
			self.expr()
			self.match(")")
		elif self.la == "identifier":
			self.match("identifier")
		elif  self.la == "TRUE" or self.la == "FALSE":
			self.boolean()
		else:
			raise ParseError("Expected ( or id or boolean") 	
	
	#boolean ->
	def boolean(self):
		if self.la == "TRUE":
			self.match("TRUE")
		elif self.la == "FALSE":
			self.match("FALSE")
		else:
			raise ParseError("Expected TRUE or FALSE")

	#or_operator ->
	def or_operator(self):
		if self.la == "OR":
			self.match("OR")
		else:
			raise ParseError("Expected OR")

	#and_operator ->
	def and_operator(self):
		if self.la == "AND":
			self.match("AND")
		else:
			raise ParseError("Expected AND")

	#not_operator 
	def not_operator(self):
		if self.la == "NOT":
			self.match("NOT")
		elif self.la == ")" or self.la == "identifier" or self.la == "TRUE" or self.la == "FALSE":
			return
		elif self,la is None:
			return
		else:
			raise ParseError("Expected NOT")
	#End of Grammar here				


	

#Create the parser object
parser = MyParser()

#Open file for parsing
with open("project2.txt","r") as fp:
	try:
		parser.parse(fp)
	except plex.error.PlexError:
		_,lineno,charno = parser.position()	
		print("Scanner Error: at line {} char {}".format(lineno,charno+1))
	except ParseError as perr:
		_,lineno,charno = parser.position()	
		print("Parser Error: at line {} char {}".format(lineno,charno+1))

