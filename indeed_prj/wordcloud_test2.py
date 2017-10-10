'''
Created on Sep 29, 2017

@author: guillermo.ziegler

* How to play with Panda and indeed Data
* Adding some complexity and loop in a list of provinces. Show all results together
* And now Word Cloud
* Simplify Code
'''

import requests
#from pandas.core.dtypes.missing import isnull
import pandas as pd
#import json
#from pprint import pprint
import sys
from test.sortperf import flush

#####################################################################################
######### FUNCTIONS DEF #############################################################
#####################################################################################
        
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
    return r.json(); #json_results 

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    #print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), sep = '', end = '\r', flush=True)
    # Print New Line on Complete
    if iteration == total: 
        print()
    return;

#####################################################################################
######### MAIN CODE##################################################################
#####################################################################################

## Defaults for Queries
DEF_START = 0
DEF_LIMIT = 10
DEF_LOCATION = 'Ottawa, ON'
DEF_QRY = 'developer'

## Query Call - Gets first Page of results
json_results = query_indeed(DEF_QRY, DEF_LOCATION, DEF_START, DEF_LIMIT)

## Evaluates results received
total_results = json_results['totalResults']
if total_results == 0:
    sys.exit('No results returned - Stopping Execution')

# I want to loop through all the results I received in total_results
# Initializing variables for loops

start =  json_results['start']-1  #because there's a difference of on between the index I need and the number that comes back in the query 
end =  json_results['end']-1
#How many times I'll have to loop based on 
pages_to_process = (divmod(total_results, DEF_LIMIT)[0])+1 if (divmod(total_results, DEF_LIMIT)[1] != 0) else divmod(total_results, DEF_LIMIT)[0]

#Initializing lists and dicts to store data
results_list = []
#result_dict = {}
url_list = [] 
page = 1

while page <= pages_to_process:
    #create list of dicts with data I want from JSON
    loop_len = end - start
    #for each page I loop through all results received
    for result in range(loop_len + 1):
        #I extract whatever I need from the json to save it to a list or dict
#        results_list.append({'location':json_results['results'][result]['formattedLocationFull'],'employer':json_results['results'][result]['company']})
        url_list.append(json_results['results'][result]['url'])
    #prepare for next query
    start = end+1
    json_results = query_indeed(DEF_QRY, DEF_LOCATION, start, DEF_LIMIT)
    start =  json_results['start']-1
    end =  json_results['end']-1
    #Once I received the new result, I have a new page to process
    page += 1

#print('How many URLs did I save in the list? %s' % (len(url_list)))
#sys.exit('************* ENDING **********************')
#while url_ndx < len(url_list):
#    print(url_list[url_ndx]) 

#I will go through the URLs in the list to get the job descriptions for each
#Now Collect URLs text
# Import requests (to download the page)
import requests
# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup
# set the headers like we are a browser,
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
content = ''    #This var to store all the text I will process in wordcloud

ndx = 0
#0% Progrss Bar
printProgressBar(0, len(url_list), prefix = 'Progress:', suffix = 'Complete', length = 50)
while ndx < len(url_list):     #I loop through all the URLs in the list
    #For each URL in the list
    #print('Requesting URL # %s' % (ndx))
    response = requests.get(url_list[ndx], headers=headers) #request the page
    #si no vuelve 200 (OK) => Aviso y sigo con el próximo
    if response.status_code != requests.codes.ok:  # @UndefinedVariable
        continue #sigo con next URL 

    #El sitio fue leido con exito
    #parse the downloaded homepage and grab all text
    soup = BeautifulSoup(response.text, "html.parser")
    #en el tag span class summary está la info que necesito
    #acumulo el texto en una variable
    content += soup.find("span", {"class":"summary"}).text
    #next URL  
    ndx += 1
    printProgressBar(ndx, len(url_list), prefix = 'Progress:', suffix = 'Complete', length = 50)

#Wordcloud section
from wordcloud import WordCloud
#import wordcloud

# Read the whole text.
#text = open(path.join(d, 'constitution.txt')).read()

# Generate a word cloud image from the content in "content"
wordcloud = WordCloud().generate(content)

# Display the generated image:
# the matplotlib way:
#import matplotlib.pyplot as plt
#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis("off")

# lower max_font_size
#wordcloud = WordCloud(max_font_size=40).generate(text)
#plt.figure()
#plt.imshow(wordcloud, interpolation="bilinear")
#plt.axis("off")
#plt.show()

# The pil way (if you don't have matplotlib)
image = wordcloud.to_image()
image.save(".\wcloud.png", "PNG")
image.show()

