'''
Created on Sep 29, 2017

@author: guillermo.ziegler

* How to play with Panda and indeed Data
* Adding some complexity and loop in a list of provinces. Show all results together

'''

import requests
#from pandas.core.dtypes.missing import isnull
import pandas as pd
#import json
#from pprint import pprint
import sys
        
def query_indeed(pquery, plocation, pstart=0, plimit=25): #RECCEIVES DATA FOR QUERY / RETURNS RESULTS IN JSON
    #print('Inside Query Function. Received query: %s, location %s, start %s, limit %s' % (pquery, plocation, pstart, plimit)) 
    url = 'https://ca.indeed.com/ads/apisearch'
    pub_id = '4192742337509875'
    query = pquery      #RECIBIR - No Default Value
    location = plocation   #RECIBIR - No Default Value
    sort = ''
    radius='' 
    site_type = ''
    job_type = ''
    start= pstart         #RECIBIR de que nro de resultado comienzo el query (DEFAULT = 0)
    limit =plimit       #RECIBIR Cuantos resultados por Query - Max 25 (DEFAULT)
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
        sys.exit('Location cannot be empty')
    
    payload = {'publisher':pub_id,'q':query,'l':location,'sort':sort,'radius':radius,'st':site_type,'jt':job_type,'start':start,'limit':limit,'fromage':fromage,'filter':fltr,'latlong':latlon,'co':country_code,'chnl':chanel,'userip':userip,'useragent':useragent,'v':version,'format':response_format}
    
    r = requests.get(url, params=payload)
    #print('Returning this: ' )
    #print(r.json())
    #print('Back to main' )
    return r.json() #json_results 

#####################################################################################

DEF_START = 0
DEF_LIMIT = 10
DEF_LOCATION = 'ON'
DEF_QRY = 'engineer'

json_results = query_indeed(DEF_QRY, DEF_LOCATION, DEF_START, DEF_LIMIT)

total_results = json_results['totalResults']
if total_results == 0:
    sys.exit('No results returned - Stopping Execution')

start =  json_results['start']-1
end =  json_results['end']-1
pages_to_process = (divmod(total_results, DEF_LIMIT)[0])+1 if (divmod(total_results, DEF_LIMIT)[1] != 0) else divmod(total_results, DEF_LIMIT)[0]
  
results_list = []
result_dict = {}
page = 1

while page <= pages_to_process:
    #create list of dicts with data I want from JSON
    loop_len = end - start
    for result in range(loop_len + 1):
        results_list.append({'location':json_results['results'][result]['formattedLocationFull'],'employer':json_results['results'][result]['company']})
    start = end+1
    json_results = query_indeed(DEF_QRY, DEF_LOCATION, start, DEF_LIMIT)
    start =  json_results['start']-1
    end =  json_results['end']-1
    page += 1

#sys.exit('************* ENDING **********************')

print('Stats for keywords ''%s'' in %s' % (DEF_QRY, DEF_LOCATION))
#With that data in the list, I create the Pandas DataFrame
df = pd.DataFrame(results_list)
#print(df)
#Now I should be able to play with the data!!
print(df['location'].value_counts())
    