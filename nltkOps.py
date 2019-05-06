#################################################################################################
# Khuram Chughtai
# NLTK Functions for ML Learning
# NLTK GEN Operations Module

# Library Imports
import os			# Used for Operating System Specific Commands
import logging		# Used for Logging Purposes to help keep track of issues
import nltk			# Overall encompassing Library for NLTK functions
# Imports Needed for the BreakUpText Function
# These Functions are used to Divide up by either sentence or text given any input string
from nltk.tokenize import word_tokenize, sent_tokenize
# Imports Needed for the removeStopWords Function 
from nltk.corpus import stopwords 	# Includes list of stop words like [a, the, etc]
from string import punctuation		# Includes all known punctuation for english language to help clean tokenized data
# For Creating the N Grams counter
from nltk.util import ngrams as nltkNGrams		# Helps to Create NGrams for each list of words provided



def lprint(listObj):
	""" 
	Creating a Function do to List Prints that has an index value and splits records per line to make it easier to view

	@param	listObj	(str)	List that I will be printing one per line
	"""
	for iterObj, item in enumerate(listObj):
		print("Iter: {},\t Raw Contents: {}".format(iterObj, item))

class NLTKops:
	"""
	Notification class that will send out either an email or text message if an error occurs
	"""
	def __init__(self, name, **kwargs):
		self.name = name                        # Name Provided for Logging Purposes 
		self.base =  str(os.path.dirname(os.path.abspath( __file__ )))
		for key in kwargs:
			# This will look at different Given Arguments Passed by a Class and process them accordingly
			if str(key).lower() == 'given_argument':
				pass
			elif str(key).lower() == 'logging':
				# The following says an argument was given where the user asked for Logging to be True
				# The following action is depricated to allow for the logging that Teradata Module Does.
				if str(kwargs[key]).lower() == "file":
					try:  # Catch Block to create a self logging instance as this is extremely Important to Submit Success or Failure
						if not os.path.exists( self.base + "/logs"):
							os.makedirs(self.base + "/logs")
						self.log = self.createLog(	application=str(self.name),
													applicationpath=str(self.base + '/logs/{}.log'.format(self.name)))
					except Exception as error:
						# The following will Raise a better error that lets us unstand it was caused by Logging Module
						raise ValueError("Not Able to Initiate Log File: {}".format(error))
				elif str(kwargs[key]).lower() == "std":
					try:  # Catch Block to create a self logging instance as this is extremely Important to Submit Success or Failure
						self.log = self.createLog(	application=str(self.name),
													applicationpath=str(self.base + '/logs/{}.log'.format(self.name)),
													stdOutput = True, fileOutput = False)
					except Exception as error:
						# The following will Raise a better error that lets us unstand it was caused by Logging Module
						raise ValueError("Not Able to Initiate Log File: {}".format(error))
				elif str(kwargs[key]).lower() == "both":
					try:  # Catch Block to create a self logging instance as this is extremely Important to Submit Success or Failure
						if not os.path.exists( self.base + "/logs"):
							os.makedirs(self.base + "/logs")
						self.log = self.createLog(	application=str(self.name),
													applicationpath=str(self.base + '/logs/{}.log'.format(self.name)),
													stdOutput = True)
					except Exception as error:
						# The following will Raise a better error that lets us unstand it was caused by Logging Module
						raise ValueError("Not Able to Initiate Log File: {}".format(error))
				
	def createLog(self, application, applicationpath, fileOutput = True, fileRotate = False, stdOutput = False):
		"""
		Base Logging Function created to write output from various functions for better error checking
		this function is for class use only and not meant to be used by outside user.\n
		
		@param  application  (str)   Name of the Logging Instance that is to be created\n
		@param  applicationpath  (str)   Path of the Logging file to which this information will be appended\n
		@param	fileOutput	(bool)	Flag to let users write log output to file
		@param	fileRotate	(bool)	Flag to set Log File Rotation in place
		@param	stdOutput	(bool)	Flag to let users stream output to standard out
		@return mylog   (loggingClass)    Logging Class instance used to write to the log file.\n
		"""
		#fileRotate = False					# Will Implement a file Rotation Policy for Logs
		mylog = logging.getLogger(application)
		if fileOutput == True:
			# If the file Rotating Flag is On then we will 
			if fileRotate == True:
				fileHandler = logging.RotatingFileHandler(applicationpath, maxBytes = (1048576*5), backupCount = 7)
				fileHandler.setFormatter(logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s'))
			else:
				fileHandler = logging.FileHandler(applicationpath)
				fileHandler.setFormatter(logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s'))
			mylog.addHandler(fileHandler)
		if stdOutput == True:			# If the Output 
			consoleHandler = logging.StreamHandler()
			consoleHandler.setFormatter(logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s'))
			mylog.addHandler(consoleHandler)
		mylog.setLevel(logging.DEBUG)
		return mylog

	def readFile(self, fileName):
		"""
		Simple Function to open up file with a WITH clause and close it after it reads the entire contents into a string.
		"""
		if os.path.exists(fileName):
			with open(fileName, 'r') as inputFile:
				return inputFile.read()
		else:
			self.log.error("File Does not exist in the given path and could not be opened")
			raise FileExistsError("File Does not exist in directory")

	def downloadNLTKPackages(self):
		"""
		This will try to execute a python file to make sure all NLTK packages are downloaded
		"""
		nltk.download('punkt')
		nltk.download('stopwords')
	
	def createListFromFile(self, fileName):
		"""
		Takes an input of Filename and reads the given file and splits it into a list of lines to be processed.  
		@param fileName (str)  The file name to open in current directory to processs

		returns list of lines from the file
		"""
		try:
			with open(self.base + "/" + fileName, 'r') as inputFile:
				myListOfLines = inputFile.read().splitlines()
				self.log.info("Read in from: {} and created a list of {} elements".format(fileName, len(myListOfLines)))
				return myListOfLines
		except Exception as error:
			self.log.error("Could not parse file: {}".format(error))

	def breakUpText(self, textInput, senOrWords, lowercase=True):
		"""
		This Function Simply uses the NLTK functions and breaks up a given text String accordingly and 
		returns the list of elements that are a result of the operations.

		@param	text	(str)	String Chunk that will be processed
		@param	senOrWords	(str)	Flag that will process and return data accordingly,
									Ex: ['sen', 'words', 'both']
		"""
		self.log.info("Received Text Input with the following length in Characters: {}".format(len(textInput)))
		self.log.info("BreakUpText Input Values: senOrWords: {}".format(senOrWords))
		
		# Converts Data to lowercase to help with ease of removing stop words
		if lowercase == True:
			text = textInput.lower()
		else:
			text = textInput
		
		# Does the Main Processing of the Function 
		if senOrWords.lower() in ['sentence','sen']:
			returnObj = sent_tokenize(text = text, language='english')
			self.log.info("Parsed text has a total of {} Sentences".format(len(returnObj)))
		elif senOrWords.lower() in ['words', 'word']:
			returnObj = word_tokenize(text=text, language='english', preserve_line=False)
			self.log.info("Parsed text has a total of {} Words".format(len(returnObj)))
		elif senOrWords.lower() in ['wordsen', "both"]:
			sentences = sent_tokenize(text = text, language='english')
			self.log.info("Parsed text has a total of {} Sentences".format(len(sentences)))
			returnObj = [word_tokenize(text=sent, language='english', preserve_line=True) for sent in sentences ]
			self.log.info(	"Number of Words in Each Sentences: {}".format( 
							["Sentence {}, Words {}".format(iterObj, len(element))
							for iterObj, element in enumerate(returnObj)]  ))
		return returnObj

	def removeStopWords(self, textList):
		"""
		This function is in place to help remove any stop words from text to help with necessary operations
		
		@param	textList	(list)	tokenized word list which you want stop words removed from.
		"""
		# We will be taking the stopwords list of english words
		# And the list of Punctuation and adding them to a set
		# We are using a set to remove dupilcates in the most efficent way
		self.log.debug("Length of stopwords {}, Length of Punctuation {}".format( 	len(stopwords.words('english')),
																				 	len(list(punctuation))))
		# Adding my personal list to remove quotes as well as they are causing issues with creating n grams
		stopWordsList =list( stopwords.words('english') + list(punctuation) + ["'",'"','``',"''"] )
		# Once the list is created we will be using a simple list comprehension method to return data
		returnObj =  [word for word in textList if word not in stopWordsList]
		self.log.info("Preprocessed List {} records, Postprocess List {} records ".format(len(textList), len(returnObj)))
		return returnObj 

	def createNGrams(self, listOfWords, **kwargs):
		"""
		Used NLTK ngram function to create ngrams from given arguments

		@param	ngram	(int)	What Ngram value should we create
		@param	returnAmount	(int)	How many of the top ngrams should be returned
		@param	returnAll	(bool)	Return all of the ngrams that are created or only a
		@param	returnCounts	(bool)	This will return the counts as well as 
		@param	returnOrder	(str)	This is asking to return sorted ngrams list in asscending or decending order
									opts ['asc', 'dsc'] 
		"""
		# Default Local Variables Established
		ngramAmount = 2
		returnAll =	True
		returnAmount = 0 
		returnCounts = False
		returnOrder = 'dsc'
		# Reading in the arguments provided by the function
		for key in kwargs:
			# This will look at different Given Arguments Passed by a Class and process them accordingly
			if str(key).lower() == 'given_argument':
				pass
			elif str(key).lower() in ['ngram', 'ngrams']:
				ngramAmount = kwargs[key]
			elif str(key).lower() == 'returnall':
				returnAll = kwargs[key]
			elif str(key).lower() == 'returnamount':
				returnAmount = kwargs[key]
			elif str(key).lower() == 'returncounts':
				returnCounts = kwargs[key]
			elif str(key).lower() == 'returnorder':
				returnOrder = kwargs[key]

		# Doing the Main processing of the Function 
		listOfNGrams = nltkNGrams(listOfWords, ngramAmount)
		listOfNGrams = list(listOfNGrams)	# Due to the function returing a generator object we need to convert to list
		self.log.info("createNGrams, Number of ngrams created from list provided: {}".format(len(listOfNGrams)))
		#We will be making a set of listOfNGrams to make it easier for us to remove duplicates and get a count
		setOfNGrams = set(listOfNGrams)
		countsOfNGrams = []			# This structure will keep a count of the NGrams to help sort
		for item in setOfNGrams:
			countsOfNGrams.append((item, list(listOfNGrams).count(item)))
		# Now we Sort the data based off the counts
		if returnOrder == 'dsc':
			countsOfNGrams.sort(key=lambda tupleValue: tupleValue[1], reverse=True)  # Sorts in place to given variables
		else:
			countsOfNGrams.sort(key=lambda tupleValue: tupleValue[1], reverse=False)  # Sorts in place to given variables
		self.log.info("createNGrams, Total Sorted NGrams list {}".format(len(countsOfNGrams)))
		####### This is the Return Portion and needs to be at the bottom of the function #########
		# Resetting the Ngram inital list to only include values and not counts
		if returnCounts == True:
			listOfNGrams = countsOfNGrams
		else:
			listOfNGrams = []
			for ngramValue in countsOfNGrams:
				listOfNGrams.append(ngramValue[0])
		# Checking to see if all ngrams are asked to be returned
		if returnAll == True:
			# Checking to see if user did not change the default value of returnAll and just gave returnAmt argument
			if returnAmount > 0:
				# If this value is greater than zero than it has been manually reset so it will return that amount
				return listOfNGrams[:returnAmount]
			else:
				# If the value is 0 or less than zero than it has not be modified or is an illegal argument
				# in which case the entire list will be returned. 
				return listOfNGrams
		elif returnAll == False:
			# We will be going into this loop if we want a specific number of ngrams returned
			if returnAmount > 0:
				# If this value is greater than zero than it has been manually reset so it will return that amount
				return listOfNGrams[:returnAmount]
			else:
				# If the value is 0 or less than zero than it has not be modified or is an illegal argument
				# in which case the entire list will be returned. 
				return listOfNGrams
		else:
			self.log.error("CreateNGrams, Reached UnExpected State with return values of ngram list")


if __name__ == "__main__":
	workerClass = NLTKops(name="Testing", logging = "both")
	#print(workerClass.readFile(fileName="samples/sample2.txt"))
	# Example 1 - With no stop Words and 2Grams to Check
	myList = workerClass.breakUpText(	textInput = workerClass.readFile(fileName="samples/sample2.txt"),
										senOrWords="words")
	myListNoStopWords = workerClass.removeStopWords(textList = myList)
	ngramList = workerClass.createNGrams(	listOfWords = myListNoStopWords, 
											returnAmount = 10,
											returnCounts = True)
	lprint(ngramList)

	#Example 2 - With Stop Words and 2Grams to Check
	myList = workerClass.breakUpText(	textInput = workerClass.readFile(fileName="samples/sample2.txt"),
										senOrWords="words")
	ngramList = workerClass.createNGrams(	listOfWords = myList, 
											returnAmount = 10,
											returnCounts = True)
	lprint(ngramList)