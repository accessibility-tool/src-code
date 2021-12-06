import requests
import json
def get_links(title, search_string="", continue_string=""):
    S = requests.Session()
    URL="https://en.wikipedia.org/w/api.php"
    PARAMS = {
            "action":"query",
            "format":"json",
            "titles":title,
            "prop":"links",
            "pllimit":"500",
            "pltitles": search_string,
        }
    if continue_string != "":
        PARAMS["plcontinue"]=continue_string

    R = S.get(url=URL, params=PARAMS)
    t=json.loads(R.text)
    #print(t)
    D = t['query']['pages']
    #print(json.loads(R.text))
    # print(D.keys())
    # print(D)
    if len(D) == 1:
        for x in D:
            if 'links' in D[x].keys():
                DATA=(D[x]['links'])
            elif 'title' in D[x].keys():
                return [D[x]['title']]

    DATA=list(map(lambda x:x['title'], DATA))
    if "continue" in t.keys():
        DATA=DATA+get_links(title, search_string, t['continue']['plcontinue'])

    def filter_foo(s):
        if s.find("Wikipedia:") == -1 and s.find("(identifier)") == -1 and s.find("Help:") == -1 and s.find("Category:") == -1 and s.find("Portal:") == -1 and s.find("Template:") == -1:
            return True
        return False

    DATA=list(filter( filter_foo , DATA))
    return DATA

#print(get_links("Apple Computer, Inc. v. Microsoft Corp.","",""))