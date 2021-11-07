import yake
import wikipediaapi

#Scraping Wikipedia for necessary data.

def wiki_scrape(topic_name):
    wiki_api = wikipediaapi.Wikipedia(language="en",extract_format=wikipediaapi.ExtractFormat.WIKI)
    page_name = wiki_api.page(topic_name)
    if not page_name.exists():
        print("Page {} doesn't exists.".format(topic_name))
    
    page_links = list(page_name.links.keys())
    result = {
        'page': topic_name,
        'text': page_name.text,
        'links': page_links
    }

    return result

#Extracting keywords from the text of the article.

def extract_keywords(text):
    kw_extractor = yake.KeywordExtractor()

    #Attributes for yake.
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.9
    numofkeywords = 200


    custom_kw_extractor = yake.KeywordExtractor(lan=language,n=max_ngram_size,dedupLim=deduplication_threshold,top=numofkeywords,features=None)

    keywords = custom_kw_extractor.extract_keywords(text)


    return keywords

#Extract the links from the important keywords.
def extract_links(keywords, links):
    result = []
    wiki_api = wikipediaapi.Wikipedia(language="en",extract_format=wikipediaapi.ExtractFormat.WIKI)
    for x in keywords:
        name = x[0]
        page_name = wiki_api.page(name)

        if page_name.exists():
            title = page_name.title
            if title in links and title not in result:
                result.append(title)
    return result

if __name__=="__main__":
    name = "GitHub"
    dict = wiki_scrape(name)
    lst = extract_keywords(dict['text'])
    lst2 = dict['links']
    ans = extract_links(lst,lst2)
    print(ans)