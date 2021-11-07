import requests
def get_subcat(title):
    S = requests.Session()
    URL="https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action":"query",
        "format":"json",
        "list":"categorymembers",
        "cmtitle":title,
        "cmtype":"subcat"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = list(map( lambda x:x['title'] ,R.json()['query']['categorymembers']))
    return DATA
