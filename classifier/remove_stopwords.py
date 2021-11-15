import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from load_data import load_all_table_data


tables = ["brightermonday", "careerpointkenya", "jobwebkenya"]


sentences  = load_all_table_data(tables)

def clean_stop_words(sentences):
    for sentence in sentences:
        sent_tokens = word_tokenize(sentence)
        token_without_sw =  [word for word in sent_tokens if not word in stopwords.words()]
    
    return token_without_sw