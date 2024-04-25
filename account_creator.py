import requests,itertools,threading,string,random,json,csv,os
from queue import Queue


HEADERS = {
    'Accept'                :'application/json',
    'Accept-Encoding'       :'gzip, deflate, br, zstd',
    'Accept-Language'       :'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control'         :'no-cache',
    'Content-Length'        :'256',
    'Content-Type'          :'application/json',
    'Origin'                :'https://ordering.digital.grilld.com.au',
    'Pragma'                :'no-cache',
    'Priority'              :'u=1, i',
    'Referer'               :'https://ordering.digital.grilld.com.au/',
    'Sec-Ch-Ua'             :'"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile'      :'?0',
    'Sec-Ch-Ua-Platform'    :'"Windows"',
    'Sec-Fetch-Dest'        :'empty',
    'Sec-Fetch-Mode'        :'cors',
    'Sec-Fetch-Site'        :'same-site',
    'User-Agent'            :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'X-Grilld-App-Platform' :'web',
    'X-Grilld-App-Version'  :'4.2.0'
    }

def start_account_create_thread(q,thread_num:int)->bool:
	while not q.empty():
		work = q.get()
		submit_request(**work)
		q.task_done()
	return True
def start_email_verify_thread(q,thread_num:int)->bool:
	while not q.empty():
		work = q.get()
		verify_email(**work)
		q.task_done()
	return True

def load_data()->dict:
    data_path = "data.json"
    try:
        with open(data_path,encoding='utf-8') as file:
            dataFile = json.loads(file.read())
    except:
        dataFile = {}
    return dataFile

def generate_email_list(username : str)->list:
    emails = list()
    username_length = len(username)
    combinations = pow(2, username_length - 1)
    padding = "{0:0" + str(username_length - 1) + "b}"
    for i in range(0, combinations):
        bin = padding.format(i)
        full_email = ""

        for j in range(0, username_length - 1):
            full_email += (username[j])
            if bin[j] == "1":
                full_email += "."
        full_email += (username[j + 1])
        emails.append(full_email + "@gmail.com")
    return emails
def request_verify_email(email:str)->bool:
    url = "https://api.digital.grilld.com.au/v1/auth/lookup"
    data = {
        "emailAddress":email,
    }
    response = requests.post(url,headers=HEADERS,data=data)
    try:
        if response.status_code == 200:
            return True
    except:
        return True
    return False
def register(dateOfBith : str, emailAddress : str, firstName : str, lastName : str, mobileNumber : str, password : str,aflTeam : str) -> bool:
    url = 'https://api.digital.grilld.com.au/v1/auth/register'

    data = {
        "emailAddress":emailAddress,
        "password":password,
        "givenName":firstName,
        "familyName":lastName,
        "mobileNumber":mobileNumber,
        "dateOfBirth":dateOfBith,
        "studentType":0,
        "preferredRestaurantId":0,
        "tags":{
            "madBunday":{
                "code":"AFL",
                "team":aflTeam
            }
        }

    }
    try:
        response = requests.post(url,headers=HEADERS,json=data)
        if response.status_code != 200:
            return False
        if (response.json()['session'] and response.json()['user']):
            return True
    except:
        return False

def generate_team_month_list()->list:
    teamList = ["Adelaide","Brisbane","Carlton","Collingwood","Essendon","Fremantle","Geelong",
                "Gold Coast","Greater Western Sydney","Hawthorn","Melbourne","North Melbourne",
                "Port Adelaide","Richmond","St Kilda","Sydney","West Coast","Western Bulldogs"]
    
    monthList = [1,2,3,4,5,6,7,8,9,10,11,12]

    return list(itertools.product(teamList,monthList))

def password_generator(size=10, chars=string.ascii_lowercase + string.digits)->str:
	return ''.join(random.choice(chars) for _ in range(size))

def submit_request(submittedAccounts : list,aflTeam : str,birthMonth : int,email: str,data : dict):
    password = password_generator()
    birthDate = f"{data['birthYear']}-{birthMonth:02d}-{random.randint(0, 27):02d}"
    account_submitted = register(birthDate,email,data['firstName'],data['lastName'],data['mobileNumber'],password,aflTeam)
    if account_submitted:
        print(f"Account [{email}] has been created!")
        submittedAccounts.append({"email":email,"password":password,"birthDate":birthDate,"aflTeam":aflTeam})
    else:
        print(f'Failed to created Account [{email}]')
    
def verify_email(verifiedEmailList: list,email:str):
    email_exists = request_verify_email(email)
    if not email_exists:
        verifiedEmailList.append(email)

def write_to_csv_file(data: list)->bool:
    with open("accounts.csv","w",newline="") as f:  
        fieldNames = ["email","password","birthDate","aflTeam"]
        cw = csv.DictWriter(f,fieldnames=fieldNames,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        cw.writeheader()
        cw.writerows(data)
    if os.path.isfile("accounts.csv"):
        return True
    return False
      

def main():
    data = load_data()
    if not data:
        print("Failed to load Data File! Please check 'data.json' exists!")
        exit()
    threadNumber = 20
    submittedAccounts = []
    team_month_list = generate_team_month_list()
    email_list = generate_email_list(str(data['email'].split("@")[0]))
    verified_email_list = []
    print('Generating Email List....')
    q = Queue(maxsize=0)
    for email in email_list:
        q.put({"verifiedEmailList":verified_email_list,"email":email})
    for i in range(threadNumber):
        worker = threading.Thread(target=start_email_verify_thread,args=(q,i))
        worker.setDaemon(True)
        worker.start()
    q.join()
    if not verified_email_list:
        print("No Email options available! Please use another Gmail!")
        exit()
    print(f"Generated Email Options. [{len(verified_email_list)}] emails available.")
    print("Creating Accounts.....")
    q = Queue(maxsize=0)
    for item in team_month_list:
        q.put({'submittedAccounts':submittedAccounts,'aflTeam':item[0],'birthMonth':item[1],"email":verified_email_list.pop(),"data":data})
    for i in range(threadNumber):
        worker = threading.Thread(target=start_account_create_thread,args=(q,i))
        worker.setDaemon(True)
        worker.start()
    q.join()
    if not submittedAccounts:
        print("Failed to generate accounts!")
        exit()
    print(f"Generated [{len(submittedAccounts)}] Accounts!")
    print("Writing to CSV file!")
    file_created = write_to_csv_file(submittedAccounts)
    if file_created:
        print("Created accounts.csv!")
    else:
         print("Failed to create accounts.csv")

main()