import pandas as pd
import tensorflow as tf
import nltk
nltk.download('stopwords')
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
class Model:
    d1 = d2 = d3 = an = int() 
    def __init__(self):
        self.load()

    def load(self):
        Model.d1=pd.read_csv('PythonBlogs(withcode).csv')
        Model.d2=pd.read_csv('CppBlogs(with code).csv')
        Model.d3=pd.read_csv('JavaBlogs(withcode).csv')
        with open('blogs_architecture.json','r') as reader:
            global the_json
            the_json = reader.read()
        Model.an=tf.keras.models.model_from_json(the_json)
        Model.an.load_weights("blogs_weights.h5")
    
    def predict(self,list_of_blogs):
        df1=Model.d1
        df2=Model.d2
        df3=Model.d3                                 
        df2=df2.rename(columns={'Blogs':'Blog'})
        dataset=pd.concat([df1,df2,df3],axis=0,ignore_index=True)
        ann=Model.an
        corpus=[]
        for i in range(len(dataset)):
          blog=re.sub('[^a-zA-Z;<<>>~]',' ',str(dataset['Blog'][i])).lower().split()
          ps=PorterStemmer()
          keywords=['while','if','for','else','do','from','as','not','in']
          new_stopwords=[  i  for i in stopwords.words('english') if not i in keywords] #Cleaning The Data
          blog=[ps.stem(words) for words in blog if not words in set(new_stopwords)]
          blog=' '.join(blog)
          corpus.append(blog)
        
        from sklearn.feature_extraction.text import TfidfVectorizer
        cv=TfidfVectorizer()                                                            
        X=cv.fit_transform(corpus).toarray()
        
        new_blog=' '.join(list_of_blogs)

        blog=re.sub('[^a-zA-Z;>><<~]',' ',str(new_blog)).lower().split()
        ps=PorterStemmer()
        keywords=['while','if','for','else','do','from','as','not','in']
        new_stopwords=[ i for i in stopwords.words('english') if not i in keywords]
        blog=[ps.stem(words) for words in blog if not words in set(new_stopwords)]
        blog=' '.join(blog)
        new_corpus=[blog]
        new_X_test=cv.transform(new_corpus).toarray()
        new_y_predict=ann.predict(new_X_test)
        result={'cpp':round(new_y_predict[0][0]*100,2),
                'java':round(new_y_predict[0][1]*100,2),
                'python':round(new_y_predict[0][2]*100,2)
                }
        
        return result



