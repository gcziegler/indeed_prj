'''
Created on Oct 6, 2017

@author: guillermo.ziegler

* Applying BSoup to indeed Job page

'''
#Now Collect URLs text
# Import requests (to download the page)
import requests
# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup
# set the headers like we are a browser,
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
content = ''
url_list = ['https://ca.indeed.com/viewjob?jk=311dec4c39697fe0&qd=P3MmKuD6JiCkSZfwf3smC9zdEEnqG7vDFcVd-hMXwoZKcHhFMH-o44vDEAoUM8JHalu-yifFTIOhZGXMz6vt8aZACpLzztmImN88h0USQJM&indpubnum=4192742337509875&atk=1brp0tdd7af61du5']
ndx = 0
total_laps = len(url_list) 
while ndx < total_laps:
    response = requests.get(url_list[ndx], headers=headers)
    
    #si no vuelve 200 (OK) => Aviso y sigo con el próximo
    if response.status_code != requests.codes.ok:  # @UndefinedVariable
        continue #sigo con next URL 

    #El sitio fue leido con exito
    #parse the downloaded homepage and grab all text, then,
    soup = BeautifulSoup(response.text, "html.parser")
    job_text = soup.find("span", {"class":"summary"})
    print(job_text.text)
    print(soup.find("span", {"class":"summary"}).text)
    ndx += 1
print(content)
