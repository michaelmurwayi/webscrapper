import nltk 
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
from load_data import load_all_table_data
stemmer = PorterStemmer()
nltk.download('punkt')


def stem_sentence(sentences):
    stemmed_sent = []
    for sentence in sentences:
        sent_tokens = sent_tokenize(sentence)
        for sent_token in sent_tokens:
            stemmed_sent.append(stemmer.stem(sent_token))
    
    return(stemmed_sent)

