import json
import asyncio
import aiohttp
from attr import dataclass
from requests.models import Response
import links_api
import time

def get_categories(urls=None):
    URL="https://en.wikipedia.org/w/api.php"

    async def fetch(session, PARAMS):
        async with session.get(URL, params=PARAMS) as response:
            try:
                data=await response.json()
                return data
            except:
                return await fetch(session, PARAMS)

    async def get_connections():
        async with aiohttp.ClientSession() as session:
            tasks=[]
            x=[]
            for url in urls:
                PARAMS = {
                    "action":"query",
                    "format":"json",
                    "titles":url,
                    "prop":"categories",
                    "cllimit":500,
                    "clprop":"hidden"
                }
                t=asyncio.ensure_future(fetch(session, PARAMS))
                tasks.append(t)
                x.append(url)
  
            return [await asyncio.gather(*tasks), x]
            
            
    #start_time = time.time()
    r=asyncio.run(get_connections())
    #print("--- %s seconds ---" % (time.time() - start_time))

    x=r[1]
    temp=r[0]

    # print(type(temp))

    final_dict={}
    for i,url in enumerate(x):
        final_dict[url]=temp[i]

    for t in final_dict:
        D = final_dict[t]['query']['pages']
        if len(D) == 1:
            for x in D:
                if 'categories' in D[x].keys():
                    DATA=(D[x]['categories'])
                elif 'title' in D[x].keys():
                    DATA=[D[x]['title']]
        #print(DATA)
        DATA=list(filter(lambda x:x is not None,list(map(lambda x: x['title'] if (type(x) is dict and "hidden" not in x.keys()) else None, DATA))))
        final_dict[t]=DATA

    return final_dict


#print(get_categories(["Spectral line"]))


