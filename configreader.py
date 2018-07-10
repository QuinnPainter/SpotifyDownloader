
#Helper file to read the config file.
#Possible return values:
#0 - file not found.
#1 - file found, but data invalid.
#an array with data in the format [username, clientid, clientsecret, redirecturi, savelocation] 

def read():
    try:
        file = open("config", "r")
    except FileNotFoundError:
        return 0
    data = file.readlines()
    if not len(data) == 5:
        file.close()
        return 1
    try:
        usefulData = list(map(lambda x: x.split("=", 1)[1].rstrip(), data)) #Loop through list, remove text before 1st equal sign, and strip whitespace
    except Exception as e:
        print ("Error occured while reading config: ")
        print (e)
        file.close()
        return 1
    file.close()
    return usefulData
    
def create():
    with open("config", "w+") as c:
        c.write("username=\nclientid=\nclientsecret=\nredirecturi=\nsavelocation=music/")