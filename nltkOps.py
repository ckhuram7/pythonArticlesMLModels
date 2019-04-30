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
from nltk.util import ngrams



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

	def breakUpText(self, text, senOrWords):
		"""
		This Function Simply uses the NLTK functions and breaks up a given text String accordingly and 
		returns the list of elements that are a result of the operations.

		@param	text	(str)	String Chunk that will be processed
		@param	senOrWords	(str)	Flag that will process and return data accordingly,
									Ex: ['sen', 'words', 'both']
		"""
		self.log.info("Received Text Input with the following length in Characters: {}".format(len(text)))
		self.log.info("BreakUpText Input Values: senOrWords: {}".format(senOrWords))
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
		stopWordsList =set( stopwords.words('english') + list(punctuation))
		# Once the list is created we will be using a simple list comprehension method to return data
		returnObj =  [word for word in textList if word not in stopWordsList]
		self.log.info("Preprocessed List {} records, Postprocess List {} records ".format(len(textList), len(returnObj)))
		return retrunObj 

	def createNGrams(self, textList, **kwargs)
if __name__ == "__main__":
	workerClass = NLTKops(name="Testing", logging = "both")
	#print(workerClass.readFile(fileName="samples/sample2.txt"))
	myList = workerClass.breakUpText(	text = workerClass.readFile(fileName="samples/sample2.txt"),
										senOrWords="both")
	