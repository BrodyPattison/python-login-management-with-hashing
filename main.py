import hashlib #library for hashing passwords for storage
import pickle #library for reading and writing dicitonary object to a text file 
import os #Library for interacting with the operating system, mainly used here to check if the credentials file exists to avoid errors

userCreds = dict() #Creates a Global dictionary variable fo storing users log in information

def main(): #main function program is anchored off

  while os.path.isfile(os.path.join(os.path.dirname(__file__), "credentials.txt")) != True: #loop that will stop the program from progressing without a credentials file

    newAcnt = input("Looks like no credentials exist, would you like to create an account to get started? (y,n)") #prompt to see if user wishes to make an account and use the program or exit
    if newAcnt == "y":
      newUser() #calls the new user function to create a new user, which will create the missing credentials file, which will allow the program to continue
    elif  newAcnt == "n":
      exit() 

  importCredentials() #calls the import credentials function
  while True: #a loop to ensure the software always returns to the main screen login menu
    loginMenu()

def importCredentials():  #import the contents of the credentials text file to a global variable
  path = os.path.join(os.path.dirname(__file__), "credentials.txt") #finds the path to the folder the file is running from which is where the credentials text file should be, then saves the path as a variable
  with open(path, "rb") as creds: #uses the pathname found in the previous line to open the credentials text file in a read mode, specifically for binary
    global userCreds #ensure the program is using the global variable and not a local variable of the same name
    userCreds = pickle.load(creds) #uses the pickle library to read the contents of the credentials text file and saves it under the userCreds variable

def loginMenu():#displays the initial logon menu
  while True:
    print("Welcome to the CIA database, Please select an option:\n1. Login\n2. Create new User\n3. exit")
    menuSelect = input(": ") #Prints the menu options for the user then prompts for a selection

    if menuSelect == "1" or menuSelect == "2" or menuSelect == "3": #Checks if selection is a valid option and asks again if it is not
      if menuSelect == "1":#login
        clearScreen() 
        loginScreen() #Takes the user to the login screen
      if menuSelect == "2":#create new user
        newUser() #takes the user to the account creation menu
      if menuSelect == "3":#exit
        clearScreen()
        exitProgram()
      break
    else:
      clearScreen()
      print("Please enter \"1\", \"2\" or \"3\"\n") #prompts the user for a valid input and loops through the function again

def loginScreen():#handles login checks
  while True:
    userName = input("Please enter your username: ") #prompt for username
    if userName in userCreds: #checks if the username is present in the credentials, will not continue if that user does not exist
      pswd = hashPswd(input(("Hello "+userName+", please input you password: "))) #Prompts user for the password, then runs the password through the hashing software, then saves the resulting hash as a variable
      if pswd == userCreds[userName]: #compares the entered passwords hash to the saved passwords hash
        userMenu(userName, pswd) #loads the user menu, passing the username and password hash to the function for further functionality (functionality is not in use but expansion is possible)
        break
      else:
        clearScreen()
        print("\n\nPassword incorrect\n\n") #if the password is wrong, this notifies the user the password was wrong and exits teh login process
        break

def newUser():#creates a new user
  clearScreen()
  print("Welcome to the user creation wizard!")
  while True:
    userName = input("Please input the username (enter \"q\" to exit): ")
    if userName == "q": #allows a user to exit the operation
      clearScreen()
      break
    elif userName in userCreds: #checks if username already exists and notifies user, then prompts again
      clearScreen()
      print("Username \""+userName+"\"already exists")
    else:
      pswd = passwordSet("new")
      if pswd == "q":
        break
      else:
        userCreds[userName] = pswd
        saveCredentials(userCreds) #saves the current user credentials variable to the text file
        clearScreen()
        break

def passwordSet(type):  #Function for setting a password, argument changes prompt displayed depending on if user is creating new account or resetting a password
  if type == "change":
    prompt = "Please input new password: (enter \"q\" to exit):"
  elif type == "new":
    prompt = "Select a password (enter \"q\" to exit): "

  while True:
    pswd1 = input(prompt) #takes the users password input
    if pswd1 == "q": #allows the user to exit the opration
      return pswd1
    pswd2 = input("Repeat the password (enter \"q\" to exit): ") #takes user input of the password again to confirm they know their new password
    if pswd2 == "q": #allows user to exit the operation
      return pswd2
    if pswd1 == pswd2: #compares the 2 passwords to confirm user knows their password
      return hashPswd(pswd1) #returns the hash of the password
    else:
      clearScreen()
      print("Passwords do not match\n") #notifies the user the passwords they enetered are not the same and re-prompts the user for password selection
      
def userMenu(userName, pswd):#displays the user menu after logon
  clearScreen()
  while True:
    print("Hello "+userName+"\nWelcome to the user menu, please select an option\n\n1. reset password\n2. logout\n3. delete account\n4. exit")
    userInput = input(": ") #Displays the user the menu of options once they are logged in and prompts for a selection
    if userInput == "1" or userInput == "2" or userInput == "3" or userInput == "4":
      if userInput == "1":#reset password
        resetPassword(userName) #passes the current username to the change password function 
      elif userInput == "2":#logout
        clearScreen()
        break #exits the function, logging the user out
      elif userInput == "3":#delete account
        deleteUser(userName) #passes the current username to the delete user function to delete the current user
        break
      elif userInput == "4":#exit
        exitProgram() #exits the program
    else:
      clearScreen()
      print("Please input \"1\", \"2\", \"3\" or \"4\"") #prompts user for a valid input then shows the menu again

def resetPassword(userName):#resets the password 
  while True:
    clearScreen()
    print("Resetting password for user: "+userName)
    pswd = passwordSet("change")
    if pswd == "q":
      break
    else:
      userCreds[userName] = pswd
      saveCredentials(userCreds)
      clearScreen()
      print("password reset")
      input("Press \"Enter\" to continue ")
      clearScreen()
      break

#delete user
def deleteUser(userName):
  clearScreen
  while True:
    areYouSure = input("You have selected to delete this account: ("+userName+")\nAre you sure you wish to proceed?\n(y/n): ")
    if areYouSure == "y":
      del userCreds[userName]
      clearScreen()
      print("Account for "+userName+" has been succesfully deleted")
      input("Press \"Enter\" to continue")
      break
    elif areYouSure == "n":
      break    


#saves credentials dictionary to external text file
def saveCredentials(userCredentials):
  path = os.path.join(os.path.dirname(__file__), "credentials.txt")
  with open(path, "wb") as creds: 
    pickle.dump(userCredentials, creds)

#Clears the console for a cleaner CLI experience
def clearScreen():
    print("\033c") #clears the console for a cleaner CLI

#saves active data then closes program
def exitProgram():
  saveCredentials(userCreds)
  exit()

def hashPswd(pswd):
  sha256 = hashlib.sha256()
  sha256.update(pswd.encode())
  return sha256.hexdigest()
  
#calls the function for the software
main()