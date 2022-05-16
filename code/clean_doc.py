# data cleaning of resume
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

df_jd = pd.read_csv('jd.csv')
df_jd_c = pd.DataFrame({'keywords': [' '.join(df_jd['keywords'].tolist())]})
df_jd_c['keywords'] = df_jd_c['keywords'].str.replace(r'[^\w\s]+', ' ')
df_jd_c['keywords'] = df_jd_c['keywords'].str.lower()
df_jd_c['keywords'] = df_jd_c['keywords'].apply(lambda x: x.encode('ascii', 'ignore').\
                                                            strip())
df_jd_c.to_csv('jd_combine.csv')

filename = 'jd_combine.csv'
file = open(filename, 'rt')
text = file.read()
file.close()

tokens = word_tokenize(text)
words = [word for word in tokens if word.isalpha()]
stop_words = stopwords.words('english')
words = [w for w in words if not w in stop_words]

porter = PorterStemmer()
stemmed = [porter.stem(word) for word in words]
#print(stemmed[:100])
df_stemmed = pd.DataFrame(data=stemmed,columns=['keywords'])
#df_stemmed.drop_duplicates(subset = "keywords", keep = 'first', inplace = True)
#df_stemmed.drop(['index'], axis = 1)
df_stemmed.to_csv("jd_stemmed.csv")
print("stemmed word saved")
df_stemmed_c = pd.DataFrame({'keywords': [' '.join(df_stemmed['keywords'].tolist())]})
df_stemmed_c.to_csv('jd_stemmed_c.csv')

