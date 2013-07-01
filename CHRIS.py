##name: CHRIS
##created on: 6/22/13
##authors: Chris, Nick, Gage, Max
##version: 0.0.0
##===================================

'''
CHRIS 0.0.0 is a voice recognition system that takes a command, checks against the command database,
interprets, and executes the command through an object-oriented and minimalistic python program. CHRIS
0.0.0 interfaces with the user through a the python shell or command line (if not through voice).
'''

data_holder={} #dictionary for storing important values in the command the user gave
CHAR_PROXIM=2 #global variable for how close a variable value in a user command should be to a keyword

try: #imports all modules
    import speech
    import pywapi
    import chrisMod
    import sys
    import time
    import string
    from datetime import datetime
except: #if user doesn't have the right modules installed, the program gives the user an error
    raise SystemError('In initialize. System failed to load appropriate frameworks')
speech.say('system initialized successfully. welcome to Chris zero point zero point zero')
#if the program got this far, everything went well. Therefore, a message that
#everything went well and the version is given

def initializeUserData():
    '''
    Should only be used in tests.
    Collects user data every time program starts.
    In official version this should store data permanently,
    not to memory.
    '''

    wantedName=False #boolean variable which states that the user is OK with his/her name or not
    while not wantedName:
        speech.say('what is your name?')
        name=speech.input() #stores user input to name variable
        speech.say('your name is ' + name)
        speech.say('is this o k with you')
        response=speech.input() #stores user response to previous question to variable
        if response=='Yes':
            wantedName=True #user is OK with name
    gender=None #creates gender variable. we dont know users gender yet (hence the None)
    doneGender=False
    while not doneGender: #same thing  as before
        speech.say(name + ', What is your sex, male or female?')
        gender=speech.input() #user's response
        if gender=='Male' or gender=='Mail': #pyspeech misinterprets 'male' for 'mail' sometimes
            pronoun='sir' #this is what CHRIS will use to refer to the user
            doneGender=True
        if gender=='Female':
            pronoun='mam'
            doneGender=True
    speech.say('O K , we\'re done')
    ret_info=[name, gender, pronoun] #returns the name, gender, and pronoun of the user in form of list
    return ret_info
    
class Listener(object):
    '''
    The Listener class accepts a command as a string. It operates on it and executes it.
    It provides for all the user prompting, as well.
    '''
    
    def __init__(self, user_pronoun):
        
##        basic information for managing data
        
        self.__userPronoun=user_pronoun
        self.__currentCommand=None

    def getListenerInfo(self):

##        returns all user related variables
        
        self.__listernerInfo={'pronoun':self.__userPronoun}
        #the reason for a dictionary of all the values is that the listener may contain more user data in a later version
        return self.__listenerInfo

    def getCurrentCommand(self):

##        returns the current command
        
        return self.__currentCommand

    def askCurrentCommand(self):

##        asks for command

        speech.say('What would you like me to do?')
        self.__currentCommand=speech.input()
        #the current command is a string once this is executed

    def executeCurrentCommand(self):

##        turns command into an object and uses Command method to look up function to perform

        try: 
            speech.say('yes '+self.__userPronoun) #'yes sir' or 'yes ma'am'
            self.__currentCommand=Command(self.__currentCommand)
            #self.__currentCommand is turned into an Command object (defined later in code)
            if self.__currentCommand.captureVars(CHAR_PROXIM)==-1:#if the command doesn't have any important variable values such as '(5) seconds'
                speech.say(self.__currentCommand.interpret(comDB()))#looks up the command in the command data base
            else: #there are important variable values
                self.__currentCommand.captureVars(CHAR_PROXIM)#finds the variable values
                self.__currentCommand.removeText()#strips the command of these values so it can be looked up
                speech.say(self.__currentCommand.interpret(comDB()))#looks up command
        except: #there may be an error in the rest of the code or the user didn't annunciate well in this case
            speech.say('i\'m sorry. I was not able to do that')
                       
class User(object):
    '''
    User class contains basic user info
    '''

    #this whole class remains unused but could be useful for controlling how
    #many commands are being used to prevent users from spamming. It could also
    #be used for managing a group of commands
    
    def __init__(self, name='', ):

##        initializes user data and collects commands
        
        self.__name=name
        self.__commands=[]

    def addCom(self, command):

##        adds a command to command list
        if not command in self.__commands:
            self.__commands.append(command)
        else:
            raise ValueError('command is already added')

    def __iter__(self):

##        method for iterating over the user commands
        
        self.count=0
        return self

    def next(self):

##        This method is internally required by the __iter__ method
        
        if self.count>=len(self.__commands):
            raise StopIteration
        for command in self.__commands:
            self.count+=1
            return self.__commands[self.count]

class Command(object):
    '''
    structure and basic functions of a command 'ojectified'
    '''

    def __init__(self, command):

##        accepts a string (command) which is the literal command the user gave
##        ex. 'what time is it'
        
        self.__commandText=command #private variable which contains the string form of the command
        Command.possible_keyWords=['seconds'] #key words that are found next to variable values
        #The possible keywords are a public list and
        
    def getCommandText(self):

##        returns the command as a string
        
        return self.__commandText

##    def charTypeInRange(self, start_index, stop_index,  schar):
##        for char in self.__commandText[start_index : stop_index]:
##            if type(char)==type(schar):
##                return True
##        else:
##            return None

    def intTypeInRange(self, start_index, stop_index):

##        returns True if there is an int is in a certain range of the command
        
        for char in self.__commandText[start_index : stop_index]:           
            try:
                test=int(char)
                return True
            except ValueError:
                pass        
        return False

##    def charType(self, start_index, stop_index, schar):
##        for char in self.__commandText[start_index : stop_index]:
##            if type(char)==type(schar):
##                return char
##        else:
##            return None

#note to self: change so that user can provide sample for wanted primitive

    def identifyInt(self, start_index, stop_index):

##            returns the int in a certain range of the command
        
        for char in self.__commandText[start_index : stop_index]:
            try:
                test=int(char)
                return char
            except ValueError:
                pass        
        return None
        
    def captureVars(self, char_proxim):

##        puts variable values in the data_holder
        
        for keyword in Command.possible_keyWords:
            start_index=(string.find(self.__commandText, keyword))-1
            end_index=start_index+len(keyword)-1
            if self.intTypeInRange(start_index-char_proxim+1, start_index):
                data_holder[keyword[0:3]]=int(self.identifyInt(start_index-char_proxim+1, start_index))
                self.ckey=str(data_holder[keyword[0:3]])
            elif self.intTypeInRange(end_index, end_index+char_proxim-1):
                data_holder[keyword[0:3]]=int(self.identifyInt(end_index, end_index+char_proxim-1))
                self.ckey=str(data_holder[keyword[0:3]])
            else:
                return -1
        #for now, we are assuming that there is only one instance of the keyword
        #in the entire command. Later we (or I) should change this.

    def removeText(self):

##        removes variable value from string so we can match the string to a string in the database (look under comDB)
        
        first_part=self.__commandText[:string.find(self.__commandText, self.ckey)-1]
        last_part=self.__commandText[string.find(self.__commandText, self.ckey)+1:]
        self.__commandText=first_part+last_part

    def interpret(self, commandLibrary):

##        returns corresponding value of the command from the comDB dictionary
        
        return commandLibrary.getComLibrary()[self.__commandText]

class comDB(object):
    '''
    Contains the command database. I decided to put this in a class because
    I might want object-type functionality later. However, I think I'll just put
    this into a data base file with a loader later on.
    '''

    def __init__(self):

##        initializes the data base. database is represented as dictionary. functions correspond the command
        
        self.__comLibrary={
            'What time is it' : chrisMod.checkTime(),
            'Shutdown in seconds' : chrisMod.shutdown(data_holder.get('sec')),
            'Shut down in seconds' : chrisMod.shutdown(data_holder.get('sec')),
            'Done' : chrisMod.returnFalse(),
            'Dawn': chrisMod.returnFalse()
        }

    def getComLibrary(self):

##        returns the command dictionary
        
        return self.__comLibrary
