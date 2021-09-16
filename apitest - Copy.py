import requests
import json
import csv
import sys

#Objective:extracting userlogin from the csv file, Input: filename.csv Output:username list 
def userlist(filename):
    user =[]
    with open(filename, 'r') as csvfile:
    # creating a csv reader object
        csvreader = csv.reader(csvfile)
          
        # extracting field names through first row
        fields = next(csvreader)
      
        # extracting each data row one by one
        for row in csvreader:
            user.append(row[1])
        print(user)
        return user

#objective: generate password for each username        
def passwordgen(email,n):
    passwordlist = []
    count = 0

    for i in range(n):
        count = count +1
        passwordlist.append('password'+str(count)+'#*')
    return passwordlist

#Objective: write the generated password and export it to a csv
def writer(email,passwordlist):
    filename = "emails.csv"
      
    # writing to csv file
    with open(filename, 'w') as file:
        # creating a csv writer object
        csvwriter = csv.writer(file)
          
        # writing the fields
        csvwriter.writerow(['email','password'])
          
        # writing the data rows
        for i in range (len(email)):
            data = []
            data.append(email[i])
            data.append(passwordlist[i])
            csvwriter.writerow(data)


#Obective: to change password of a set of users using the okta Put password API Input:username and password Output: confirmation and password change time in UTC
def oktaapi(email,passwordlist):
    
    key = 'api_key'
    my_headers = {'Authorization':'SSWS'+key,'Accept':'application/json','Content-Type':'application/json'}

    #looping over all the users in the email list now
    for i in range(len(email)):
        user = email[i]
        password = passwordlist[i]
        BODY = {'credentials': {'password':{'value':password}}}
        response = requests.put(url ='https://your-okta-url/api/v1/users/'+user,headers = my_headers,data = json.dumps(BODY))
        data = response.json()
        if response.ok:
            #name =data['id']
            profile = data['profile']['login']
            passwordchange = data['passwordChanged']
            #status = data['status']
            print(profile +' password changed at '+ passwordchange )
        else:
            print(data['errorSummary'])

#driver function Input : filename using cmd Output : confirmationa and password change time in UTC
def main():
    filename = sys.argv[1]
    email=userlist(filename)
    n = len(email)
    passwordlist = passwordgen(email,n)
    writer(email,passwordlist)
    oktaapi(email,passwordlist)

if __name__ =='__main__':
    main()
