'''
Created on Sep 29, 2017

@author: guillermo.ziegler

* How to send a request to indeed and store the JSON/XML answer
* Del PHP del Blog

url = 'https://ca.indeed.com/ads/apisearch?publisher=4192742337509875&q=chemical%20technologist&l=Canada&sort=&radius=&st=&jt=&start=&limit=&fromage=&filter=&latlong=1&co=us&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2&format=json'

'''

import requests
from pandas.core.dtypes.missing import isnull
#import json
#from pprint import pprint
'''
url = 'https://ca.indeed.com/ads/apisearch'
pub_id = '4192742337509875'
query = ''
location = 'ON'
sort = ''
radius=''
site_type = ''
job_type = ''
start=26
limit =25
fromage = 1
fltr=1
latlon=1
country_code = 'CA'
chanel = ''
userip = '0.0.0.0'
useragent = 'Mozilla'
version=2
response_format='json'

payload = {'publisher':pub_id,'q':query,'l':location,'sort':sort,'radius':radius,'st':site_type,'jt':job_type,'start':start,'limit':limit,'fromage':fromage,'filter':fltr,'latlong':latlon,'co':country_code,'chnl':chanel,'userip':userip,'useragent':useragent,'v':version,'format':response_format}

r = requests.get(url, params=payload)
'''
'''
r.json is the JSON content of the response

print(r.json())
'''

'''
Print Answers in results

for item in r.json()['results']:
    print(item)
'''
   
'''
Print Cities

    
query_result = r.json()
for i in range(query_result['end']):
    print(query_result['results'][i]['formattedLocation'])
'''
    
'''
'totalResults': 1096, 'start': 1, 'end': 25, 'pageNumber': 0
Cuántas Páginas? 
1096/25 = 43.84 => 43 Paginas * 25 Resultados + 1 de 0.84 * 25 = 21
divmod(1096, 25) => (43, 21)
divmod('totalResults'/'end') => (Total Paginas, Resultados en Pag adicional) 
'jobtitle': 'Oil Museum Assistant', 'company': 'County of Lambton', 'city': 'Oil Springs', 'state': 'ON'
 'url': 'https://ca.indeed.com/viewjob?jk=6e
 'jobkey': '6e4da64966ff62df', 

total_results = query_result['totalResults']
start =  query_result['start']
end =  query_result['end']
pg_nmbr = query_result['pageNumber']
pages_to_loop = (divmod(total_results, end)[0])+1 if (divmod(total_results, end)[1] != 0) else divmod(total_results, end)[0] 
'''
'''
*****************************************************************************
Stats sobre: City/Prov (formattedLocation) & Employers (company)    
*****************************************************************************
'''
#Read Json and set every result in a dictionary inside a list
'''
results_list = []
result_dict = {}
#create list of dicts with data I want from JSON
for item in range(r.json()['end']):
    results_list.insert(item,{'location':r.json()['results'][item]['formattedLocationFull'],'employer':r.json()['results'][item]['company']})
#With tha data in the list, I create the Pandas DataFrame
import pandas as pd
df = pd.DataFrame(results_list)
#print(df)
#Now I should be able to play with the data!!
print(df['location'].value_counts())
'''
'''
*****************************************************************************
Loop para todas las páginas    
*****************************************************************************
'''
url = 'https://ca.indeed.com/ads/apisearch'
pub_id = '4192742337509875'
query = ''
location = 'Kanata, ON'
sort = ''
radius=15
site_type = ''
job_type = ''
start=1 #de que nro de resultado comienzo el query
limit = ''  #Cuantos resultados por Query - Max 25
fromage = 1
fltr=1
latlon=1
country_code = 'CA'
chanel = ''
userip = '0.0.0.0'
useragent = 'Mozilla'
version=2
response_format='json'

if not location:
    import sys
    sys.exit('Location cannot be empty')

payload = {'publisher':pub_id,'q':query,'l':location,'sort':sort,'radius':radius,'st':site_type,'jt':job_type,'start':start,'limit':limit,'fromage':fromage,'filter':fltr,'latlong':latlon,'co':country_code,'chnl':chanel,'userip':userip,'useragent':useragent,'v':version,'format':response_format}

r = requests.get(url, params=payload)
json_results = r.json()
print(json_results)

total_results = json_results['totalResults']
print('Total Results to Process: ' + str(total_results))
'''
if total_results > 0:
    start =  json_results['start']
    end =  json_results['end']
    pg_nmbr = json_results['pageNumber']
    pages_to_loop = (divmod(total_results, end)[0])+1 if (divmod(total_results, end)[1] != 0) else divmod(total_results, end)[0]
    
    results_list = []
    result_dict = {}
    for pg_nmbr in range(pages_to_loop):
        #create list of dicts with data I want from JSON
        for start in range(end):
            results_list.insert(start,{'location':json_results['results'][start]['formattedLocationFull'],'employer':json_results['results'][start]['company']})
        start = (limit * pg_nmbr) + 1
        pg_nmbr += 1
        payload = {'publisher':pub_id,'q':query,'l':location,'sort':sort,'radius':radius,'st':site_type,'jt':job_type,'start':start,'limit':limit,'fromage':fromage,'filter':fltr,'latlong':latlon,'co':country_code,'chnl':chanel,'userip':userip,'useragent':useragent,'v':version,'format':response_format}
'''