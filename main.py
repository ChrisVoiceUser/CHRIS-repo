from CHRIS import * #imports everything from CHRIS.py
USER_DATA=initializeUserData() #user credentials
listener=Listener(USER_DATA[2]) #initializes listener so we can use its methods
user=User(USER_DATA[1]) #here for future purposes
while True:#keep looping until user if finished
    listener.askCurrentCommand()
    listener.executeCurrentCommand()
    

