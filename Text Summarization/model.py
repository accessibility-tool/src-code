import wikipediaapi
import re
from transformers import BartForConditionalGeneration, BartTokenizerFast #BartConfig
import time

def get_summary(page_name):

    #Getting Text.
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(page_name)
    text = page.text

    #Cleaning Text.
    text = re.sub(r'==.*?==+','',text)
    text = text.replace('\n','')

    #Getting tokenizer and model
    tokenizer=BartTokenizerFast.from_pretrained('facebook/bart-large-cnn')
    model=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    inputs = tokenizer.batch_encode_plus([text],return_tensors='pt',truncation=True)
    summary_ids = model.generate(inputs['input_ids'], early_stopping=True)

    bart_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return bart_summary

#For testing purposes
# if __name__=="__main__":
#     start_time = time.time()
#     page = 'John Balliol'
#     summary = get_summary(page)
#     print(summary)
#     print("----%s seconds-----" % (time.time()-start_time))
