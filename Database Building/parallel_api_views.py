import json
import asyncio
from re import T
import aiohttp
import links_api

def sort_links_with_views(titles):
    URL="https://en.wikipedia.org/w/api.php"
    #titles=links_api.get_links("Philosophy","")
    # titles=["GitHub", "Latin", "Microsoft"]
    results = {}

    async def fetch(session, PARAMS):
        async with session.get(URL, params=PARAMS) as response:
            try:
                data=await response.json()
                return data
            except:
                return await fetch(session, PARAMS)


    def get_tasks(session):
        tasks = []
        for title in titles:
            PARAMS = [
                ("action","query"),
                ("format","json"),
                ("titles",title),
                ("prop","pageviews"),
                ("pvipdays","30")
            ]
            tasks.append(fetch(session, PARAMS))
        return tasks

    async def get_symbols():
        async with aiohttp.ClientSession() as session:
            tasks = get_tasks(session)
            responses = await asyncio.gather(*tasks)
            return responses

    r=asyncio.run(get_symbols())

    c=0
    for i,R in enumerate(r):
        c=c+1
        for x in R['query']['pages']:
            DATA=R['query']['pages'][x]['pageviews']

        sum=0
        for x in DATA:
            if DATA[x] is not None:
                sum=sum+DATA[x]

        results[titles[i]]=sum

    print("count:")
    print(c)

    def views(name):
        return results[name]

    titles=sorted(titles, key=views, reverse=True)
    #print(titles)
    return titles
