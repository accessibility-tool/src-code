#Library import
import requests
import wikipedia
import wikipediaapi

#function for view count and categories.
def get(name: str):
    #Get categories.
    # page = wikipedia.page(name)
    # lst = page.categories

    #Get view count.
    #User Agent to request from the site.
    HEADERS = {
        'User-agent': 'Attempt-user-agent'
    }

    #Modified URL to return view count for september 2021.
    URL = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/{page}/monthly/20210901/20211010'

    r = requests.get(url=URL.format(page=name),headers=HEADERS)
    data = r.json()
    try:
        view_count = data['items'][0]['views']
    except:
        print('Doesn\'t exist.')
        view_count = -1

    #Converting to a json/dictionary format
    result = {
        'view_count': view_count,
        #'categories': lst
    }

    return result

#function for categories.
#def get_category(name: str):

def page_links(name: str):
    page = wikipedia.page(name)
    lst = page.links
    #wiki_wiki = wikipediaapi.Wikipedia('en')
    #ans = []
    #i = 0
    # for link in lst:
    #     i+=1
    #     print(i)
    #     page_py = wiki_wiki.page(link)
    #     if page_py.exists():
    #         ans.append(link)
    return lst