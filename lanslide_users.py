##from urllib import request
##
##url = "https://events.lanslide.com.au/v25/?show=registrations"
##res = request.urlopen(url)
##
##print(res.read())

import requests
from bs4 import BeautifulSoup
import json
from tornado import ioloop, httpclient

url = "https://events.lanslide.com.au/v25/?show=registrations"
res = requests.get(url).text

soup = BeautifulSoup(res, "lxml")

user_table = soup.find("tbody")
users = user_table.findAll("tr", attrs={"class":""})

counter = 0
i = 0
males = 0
females = 0
unknown = 0

page_links = []

all_user_data = []

def get_pages(page_links):
    global i,males,females,unknown
    http_client = httpclient.AsyncHTTPClient(force_instance=True,defaults=dict(user_agent="Mozilla/5.0"),max_clients=20)
    for link in page_links:
        global i
        i += 1
        http_client.fetch(link.strip(),handle_response, method='GET',connect_timeout=10000,request_timeout=10000)
    ioloop.IOLoop.instance().start()
    print("Males: {0} \n Females: {1} \n Unknown: {2}".format(males,females,unknown))
 
def handle_response(response):
    if response.code == 599:
        print(response.effective_url,"error")
        http_client.fetch(response.effective_url.strip(), handle_request, method='GET',connect_timeout=10000,request_timeout=10000)
    else:
        global i,males,females,unknown
        html = response.body.decode('utf-8')
        json_file = json.loads(html)
        gender = json_file['gender']
        
        if gender == "male":
            males += 1
        elif gender == "female":
            females += 1
        else:
            unknown += 1
        i -= 1
        if i == 0:
            ioloop.IOLoop.instance().stop()
            
for user in users:
    data = user.findAll("td", attrs={"class":"section-dark"})
    name_data = data[1].text.split(" (")

    pos = data[0].text
    username = name_data[0].strip()
    name = name_data[1][:-1].strip()
    firstname = name.split()[0]
    status = data[2].text.split(" ")[-1].strip().strip(")").strip("(")
    
    counter += 1
    url = "https://gender-api.com/get?name={}&key=DZbBvnSAYeSEHPcWHJ".format(firstname)
    page_links.append(url)
    data = [pos,username,name,firstname,status]
    all_user_data.append(data)
    #url = "https://gender-api.com/get?name={}&key=DZbBvnSAYeSEHPcWHJ".format(firstname)
    #res = requests.get(url).text
    #json_file = json.loads(res)
    #gender = json_file['gender']
           
get_pages(page_links)
print(all_user_data)

