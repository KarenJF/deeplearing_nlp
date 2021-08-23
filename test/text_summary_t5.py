# import pacakge
import json
import pandas as pd
import numpy as np
from pandas import json_normalize
import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize

from gensim.models import Word2Vec
from scipy import spatial
import networkx as nx

# t5 module
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

# setting for easy viewing
pd.options.display.max_columns = 200

############################
# Step 1: load in dataset  #
# a. load dataset.         #
# b. check dataset.        #
# c. pick interested field #
############################
# hard coded location for now
data_dir = '../data/data/'
file_name = 'car_accident_ill_1930_2020.json'

def load_data(data_dir, file_name):

    # a. load dataset
    with open(data_dir + file_name) as f:
        car_case = json.load(f)

    a = car_case['results']
    df = json_normalize(a)       

    # b. Make sure the casebody.status == 'ok' 
    # make sure data is downloaded properly
    # if casebody.status != 'ok', there will be no case details

    df2 = df[df['casebody.status'] == 'ok'].reset_index(drop = True)

    ##########################
    # c. pick useful columns # 
    ##########################
    # a. pick useful columns from caselaw meta data
    df_filter = df2[['id',
               'frontend_url',
               'decision_date',
               'jurisdiction.name_long', 
               'court.name', 
               'analysis.word_count', 
               'analysis.ocr_confidence',
               'analysis.cardinality',
               'analysis.pagerank.percentile',
               'analysis.pagerank.raw',
               'analysis.sha256',
               'analysis.simhash',
               'citations',
               'cites_to',
               'casebody.status', 
               'casebody.data.parties', 
               'casebody.data.attorneys',
               'preview',
               'casebody.data.opinions']].copy()

    # b. Get case content and author from the text
    df_filter['case_content'] = df_filter['casebody.data.opinions'].apply(lambda x: x[0]['text'])
    df_filter['case_author'] = df_filter['casebody.data.opinions'].apply(lambda x: x[0]['author'])

    # c. extract case preview from original meta data
    df_filter['clean_preview'] = df_filter['preview'].apply(lambda x: [re.sub('<[^>]+>','', i) for i in x])
    df_filter['clean_preview'] = df_filter['clean_preview'].apply(lambda x: ' '.join(x))

    return df_filter

###############################
# Step 2: Data Preprocessing  #
###############################
def remove_multiple_strings(cur_string, replace_list):
    for cur_word in replace_list:
        cur_string = cur_string.replace(cur_word, '')
    
    return cur_string

def data_preprocess(df_filter):
    df_clean = df_filter.copy()
    
    # a. take out citations - not useful for text summary
    df_clean['citation_list'] = df_clean['citations'].apply(lambda row: [i['cite'] for i in row])
    df_clean['cites_to_list'] = df_clean['cites_to'].apply(lambda row: [i['cite'] for i in row])
    df_clean['remove_citation_list'] = df_clean['citation_list'] + df_clean['cites_to_list']

    df_clean['case_content2'] = df_clean.apply(lambda row: remove_multiple_strings(row['case_content'], row['remove_citation_list']), axis = 1)

    # b. Remove punctuations and special characters from the text
    df_clean['case_content_dl'] = df_clean['case_content2'].apply(lambda x: re.sub('[^\w\s,.-]','',x))

    # c. convert all alphabets into lower case
    df_clean['case_content_dl'] = df_clean['case_content_dl'].apply(lambda x: x.lower())

    # d. (optional - No use so far) remove stopwords
    '''
    stop_words = set(stopwords.words('english'))
    df_clean['case_content_dl'] = df_clean['case_content_dl'].apply(lambda x: ' '.join([word for word in x.split(' ') if word.lower() not in stop_words]))
    '''
    return df_clean

############################################################
# Step 3: Loading T5 Deeplearning for text Summarization   #
# pretrain model usually save: ~/.cache/torch/transformers #
# or follow link below to manually download the model      #
# https://stackoverflow.com/questions/64001128/load-a-pre-trained-model-from-disk-with-huggingface-transformers                              #

########################################################
# manual download method                               # 
# Step 1: load model from huggingface.                 # 
# Step 2: save model and tokenizer to local directory  #
# Step 3: load back model from local                   #
########################################################
'''
model = T5ForConditionalGeneration.from_pretrained("t5-large")
tokenizer = T5Tokenizer.from_pretrained("t5-large")

tokenizer.save_pretrained('./model/t5_large/')
model = model.save_pretrained('./model/t5_large/')

# step 3: load back from local
tokenizer = T5Tokenizer.from_pretrained("/Users/karenfang/Documents/git_repo/legaltech/model/t5_large/")
model = T5ForConditionalGeneration.from_pretrained('/Users/karenfang/Documents/git_repo/legaltech/model/t5_large/')
'''

#######################################
# Step 4: Use t5 to summarize content #
#######################################
def generate_single_case_summary(row):
    torch.manual_seed(0)
    
    # make format for T5 model 
    preprocess_text = row.strip().replace("\n","")
    t5_prepared_Text = "summarize: "+preprocess_text
    
    # set inputs = the single case
    inputs = tokenizer.encode(t5_prepared_Text,
                              return_tensors='pt',
                              max_length=512,
                              truncation=True
                         )
    
    # beam search method - keep parameter like this for now. So far best parameters for summarization I found. 
    summary_ids = model.generate(inputs, 
                                 max_length=512, 
                                 min_length=100, 
                                 length_penalty=3., 
                                 num_beams=6,
                                 no_repeat_ngram_size=3,
                                 early_stopping=True
                                )
    
    # decode summarization from T5
    summary = tokenizer.decode(summary_ids[0])
    return summary

    
if __name__ == "__main__":
    
    # hard coded location for now
    data_dir = '../data/data/'
    file_name = 'car_accident_ill_1930_2020.json'
    # Step 1: load in caselaw data 
    df_filter = load_data(data_dir, file_name)
    
    # Step 2: Data Preprocessing
    df_clean = data_preprocess(df_filter)
    
    # Step 3: load in t5-large model 
    tokenizer = T5Tokenizer.from_pretrained("/Users/karenfang/Documents/git_repo/legaltech/model/t5_large/")
    model = T5ForConditionalGeneration.from_pretrained('/Users/karenfang/Documents/git_repo/legaltech/model/t5_large/')
    
    # Step 4: Use t5 to summarize case content
    # temperary just test with 20 cases
    test = df_clean.head(20)
    test.loc[:,'case_summarization'] = test['case_content_dl'].apply(lambda row: generate_single_case_summary(row))
    
    # Step 5: Save case summarization dataset
    test.to_pickle('./data/case_law_summary_test.pkl')
    
'''
#tf.random.set_seed(0)
torch.manual_seed(0)
text = df3['case_content_dl'][0]
preprocess_text = text.strip().replace("\n","")
t5_prepared_Text = "summarize: "+preprocess_text

inputs = tokenizer.encode(t5_prepared_Text,
                          return_tensors='pt',
                          max_length=512,
                          truncation=True
                         )
# beam search method
summary_ids = model.generate(inputs, 
                             max_length=512, 
                             min_length=100, 
                             length_penalty=3., 
                             num_beams=6,
                             no_repeat_ngram_size=3,
                             early_stopping=True
                            )

summary = tokenizer.decode(summary_ids[0])
summary

text2 = df3['case_content2'][0]
preprocess_text2 = text2.strip().replace("\n","")
t5_prepared_Text2 = "summarize: "+preprocess_text2

inputs = tokenizer.encode(t5_prepared_Text2,
                          return_tensors='pt',
                          max_length=512,
                          truncation=True)

summary_ids2 = model.generate(inputs, 
                               max_length=512, 
                               min_length=80, 
                               length_penalty=3., 
                               num_beams=6,
                               no_repeat_ngram_size=3,
                               early_stopping=True)
summary2 = tokenizer.decode(summary_ids2[0])

summary2
'''