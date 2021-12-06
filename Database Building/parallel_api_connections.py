import json
import asyncio
import aiohttp
from attr import dataclass
from requests.models import Response
import links_api
import time

def parallel_api_connections(seed=None, url_list=None):
    URL="https://en.wikipedia.org/w/api.php"
    if url_list is None or len(url_list) == 0:
        urls=links_api.get_links(seed,"","")
    else:
        urls=url_list

    if seed is not None:
        search_strings=[seed]
    else:
        search_strings=[urls[0]]

    count=0
    search_string=urls[0]
    count=1
    for y in urls:
        search_string=search_string+'|'+y
        count=count+1
        if count>=49:
            search_strings.append(search_string)
            count=0
            search_string=urls[0]
    else:
        search_strings.append(search_string)

    print(len(urls))
    print(len(search_strings))
    #print(urls)

    for i, search_string in enumerate(search_strings):
        search_strings[i]=search_string.replace(" ", "_")


    async def fetch(session, PARAMS, sem):
        async with session.get(URL, params=PARAMS) as response:
            try:
                data=await response.json()
                return data
            except:
                return await bound_fetch(session, PARAMS, sem)

    async def bound_fetch(session, PARAMS, sem):
    # Getter function with semaphore.
        async with sem:
            return await fetch(session, PARAMS, sem)

    async def get_connections():
        async with aiohttp.ClientSession() as session:
            tasks=[]
            x=[]
            sem = asyncio.Semaphore(200)
            for url in urls:
                for search_string in search_strings:
                    PARAMS = {
                        "action":"query",
                        "format":"json",
                        "titles":url,
                        "prop":"links",
                        "pllimit":"500",
                        "pltitles": search_string,
                    }
                    t=asyncio.ensure_future(bound_fetch(session, PARAMS, sem))
                    tasks.append(t)
                    # if url=="Apple Computer, Inc. v. Microsoft Corp.":
                    #     print(await t)
                    x.append(url)
  
            return [await asyncio.gather(*tasks), x]
            
            
    #start_time = time.time()
    r=asyncio.run(get_connections())
    #print("--- %s seconds ---" % (time.time() - start_time))
    #print(len(r[0]))

    x=r[1]
    temp=r[0]
    r={}
    # print(type(temp))
    for url in x:
        r[url]=[]

    for i,url in enumerate(x):
        # if url=="Apple Computer, Inc. v. Microsoft Corp.":
        #     print(temp[i], len(r[url])) 
        r[url].append(temp[i])

    c=0
    final_dict={}
    for url in r:
        for R in r[url]:
            if R is not None:
                c+=1
                # R=R.result()['query']['pages']
                R=R['query']['pages']
                if url not in final_dict.keys():
                    final_dict[url]=[]
                for x in R:
                    if 'links' in R[x].keys():
                        DATA=(R[x]['links'])
                        DATA=list(map(lambda x:x['title'], DATA))
                        #print("{}:{}".format(url,DATA))
                        final_dict[url]=final_dict[url]+DATA
                    elif 'title' in R[x].keys():
                        #print("{}:{}".format(url,R[x]['title']))
                        final_dict[url]=final_dict[url]+[R[x]['title']]


    print("count:")
    print(c)
    return final_dict

# c=0
# x=parallel_api_connections("GitHub")
# for t in x:
#     c=c+len(x[t])
#     print(len(x[t]))
# #     print(t)
# #     if t=="Apple Computer, Inc. v. Microsoft Corp.":
# #         print(x[t])


# print(c, len(x))