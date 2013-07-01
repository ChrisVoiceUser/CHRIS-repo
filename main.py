from CHRIS import * #imports everything from CHRIS.py
USER_DATA=initializeUserData() #user credentials
listener=Listener(USER_DATA[2]) #initializes listener so we can use its methods
user=User(USER_DATA[1]) #here for future purposes

while True:#infinite loop
    speech.say('you can exit by saying, done')
    listener.askCurrentCommand()
    if listener.getCurrentCommand()=='Dawn' or listener.getCurrentCommand()=='Don' or listener.getCurrentCommand()=='Done': #user says 'done' to end
        speech.say('goodbye')
        break #exits the infinite loop
    else: #if the current command is something other than done, that means it is an actual command
        listener.executeCurrentCommand()

  

