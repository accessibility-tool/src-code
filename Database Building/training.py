import nltk
import numpy as np
import random
import string
import wikipediaapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def train(page_name):
    wiki = wikipediaapi.Wikipedia(
        language="en",
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    print(page_name)
    page = wiki.page(page_name)
    text = page.text
    print("Text Extracted")

    text = text.lower()
    #nltk.download('punkt')
    #nltk.download('wordnet')

    global sent_tokens
    sent_tokens = nltk.sent_tokenize(text)
    lemmer = nltk.stem.WordNetLemmatizer()

    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]
    remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
    GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

    def greeting(sentence): 
        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)

    def response(user_response):
        robo_response = ''
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        
        if(req_tfidf==0):
            robo_response=robo_response+"I am sorry! I don't understand you"
            return robo_response
        else:
            robo_response = robo_response+sent_tokens[idx]
            return robo_response

    print('Bot Trained')

    global word_tokens
    word_tokens = nltk.word_tokenize(text)

    global getResponse
    def getResponse(userText):
        if(userText!="bye"):
            if(userText=="thanks" or userText=="thank you"):
                return("You are welcome.")
            else:
                if(greeting(userText)!=None):
                    return greeting(userText)
                else:
                    sent_tokens.append(userText)
                    #print(sent_tokens[:2])
                    global word_tokens
                    word_tokens = word_tokens + nltk.word_tokenize(userText)
                    final_words = list(set(word_tokens))
                    x = response(userText)
                    sent_tokens.remove(userText)
                    return x
        else:
            return "Bye! Take Care!"