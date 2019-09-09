import json_lines
import json
from nltk.stem.snowball import SnowballStemmer
from elasticsearch import Elasticsearch
import numpy as np

#Pointing to elastic search, initialising the port
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#Function es_indexing creates index in elastic search, we read the JSON File using json_lines.reader(), we dump and load data using json package.
#es.index has 4 parametersindex name, doc type, document number and the query.  
def indexing():
    #Reading the jsonl file
    with open('sample-1M.jsonl', 'rb') as f:
        i=1
        
        #Indexing 10000 values
        for item in json_lines.reader(f):
            if(i>=5000):
                continue
            else:

                #Converting string formatted data to json file format
                item = json.dumps(item)

                #Reading the file in order to load it to the elasticsearch
                decoded = json.loads(item)

                #Adding to the index
                es.index(index='news_article', doc_type='articles',id = i, body = decoded)
            i+=1
    
#Function es_Summary used to display document information
def es_summary(res):
    for doc in res['hits']['hits']:
        print("Document Index is:", doc['_id'])
        print("Document Search score is:", doc['_score'])
        print("Document Media type:", doc['_source']['media-type'])
        print("Document Title:", doc['_source']['title'])
        print("Source:", doc['_source']['source'])
        print("Published on:", doc['_source']['published'])
        print("Document Content:", doc['_source']['content'],'\n')
        
#Function es_search_by_index is used to test index when elastic index first indexes files. 
def search_by_index(ids):

    res=es.search(index='news_article', doc_type='articles', id=ids,body=decoded)
    return res

#Query search will search documents for given set of queries. Usercan choose queries of by choice.
def query_search(ch):    
    if ch=='1':
        title=input('Enter the Title:')
        start=input('Enter the Published Start Date(YYYY/MM/DD):')
        end=input('Enter the Published End Date(YYYY/MM/DD):')
        res = es.search(index="news_article", doc_type="articles", body={"query":{"bool":{"should":[{"match":{"title":title}},{"range":{"published":{"gte": start,"lte": end,"format": "yyyy/MM/dd||yyyy"}}}]}}},size=5000)
    if ch=='2':
        title=input('Enter the Title:')
        content=input('Enter the content phrase:')
        res=es.search(index="news_article",doc_type="articles",body={"query":{"bool":{"should":[{"match":{"title":title}},{"match":{"content":content}}]}}},size=5000)
    if ch=='3':
        media=input('Enter the Media-type:')
        content=input('Enter the content phrase:')
        start=input('Enter the Published Start Date(YYYY/MM/DD):')
        end=input('Enter the Published End Date(YYYY/MM/DD):')
        res = es.search(index="news_article", doc_type="articles", body={"query":{"bool":{"should":[{"match":{"media-type":media}},{"match":{"content":content}},{"range":{"published":{"gte": start,"lte": end,"format": "yyyy/MM/dd||yyyy"}}}]}}},size=5000)
    if ch=='4':
        title=input('Enter the Title:')
        content=input('Enter the content start phrase:')
        res=es.search(index="news_article",doc_type="articles",body={"query":{"bool":{"should":[{"match":{"title":title}},{"match_phrase_prefix":{"content":content}}]}}},size=5000)
    if ch=='5':
        title=input('Enter the Exact Title:')
        res=es.search(index="news_article",doc_type="articles",body={"query":{"match_phrase":{"title":title}}},size=5000)
    if ch=='6':
        keyword=input('Enter Query Keyword:')
        res=es.search(index="news_article",doc_type="articles",body={"query": {"multi_match":{"query":keyword,"fields": ["content^2", "title"]}}},size=5000)
    if ch=='7':
        content = input("enter the letter:")
        content = content + "*"
        res = es.search(index="news_article", doc_type="articles", body={"query":{"wildcard": {"content": content}}},size=5000)
    if ch=='8':
        source=input('Enter the Source:')
        content=input('Enter the content phrase:') 
        res=es.search(index="news_article",doc_type="articles",body={"query":{"bool":{"should":[{"match":{"source":source}},{"match":{"content":content}}]}}},size=5000)
    if ch=='9': 
        query=input('Enter the query:')
        res=es.search(index="news_article",doc_type="articles",body={"query":{"match":{"content":{"query":query,"operator":"and"}}}},size=5000)
    if ch=='10':
        query=input('Enter the query:')
        res=es.search(index="news_article",doc_type="articles",body={"query":{"match":{"content":{"query":query,"operator":"or"}}}},size=5000)
    return res

                 
#mapr function is used to carry mean avg precision and recall
def mapr(prec,recall):
    
    #initially, we set precision and recall to 0, and avg precision and recall to 0, if search hit is found,we update both features.
    #precision gives, relevant documents that were returned, recall gives documents returned as of all documents.
    averagepre=0.0
    averagerec=0.0
    c=0
    
    #the for loop below shows, if there is relevant document(1) then c will go up by 1, c here is next relevant document,
    #precision and recall will be updated for every document, as per new document found
    print('Document Count\tPrecision\tRecall\tRelevancy')
    for i in range (1,5001):
        if totallist1[i]==1:
            prec+=1.0
            recall+=1.0
            temp=prec/(i+1)
            averagepre+=temp
            temper=recall/5000
            temp=round(temp,5)
            temper=round(temper,5)
            averagerec+=temper
            if(orderedsearch[c]==orderedsearch[-1]):
                print(i+1,temp,temper,orderedsearch[c])
            
            elif(orderedsearch==[]):
                print(i+1,temp,temper,0)
            else:
                print(i+1,temp,temper,orderedsearch[c])
                c+=1
        #else precision and recall value will be same and document number keeps increasing
        else:
            temp=prec/(i+1)
            temper=recall/5000
            averagepre+=temp
            averagerec+=temper
            if(orderedsearch==[]):
                print(i+1,temp,temper,0)
            else:
                print(i+1,temp,temper,orderedsearch[c])
                
    #We find mean numberof precision and recall and avg them. 
    print('Mean Average Precision:',(averagepre/5000))        
    print('Mean Average Recall:',(averagerec/5000))


index=input('Is the file Indexed in Elastic Search?')
if(index=='no' or index=='No'):                  
    indexing()       

ch=input('Would you like to query the search engine? press y/n:')
while( ch == "y"):
    print("\n1.Searching for word through title ranged using published date:")
    print("2.Title and content is asked:")
    print("3.Media type and content range of published date:")
    print("4.Any title but content should contain start phrase:")
    print("5.Title should be exact")
    print("6.Content have higher importance than title:")
    print('7.content should begin with a letter:')
    print("8.Source and content is asked:")
    print("9.Enter 2 keywords, will return if both words appear togather in content:")                  
    print("10.Enter 2 keywords, will return if both words appear together or seperately in content:")
    ch=input('Enter a choice of query:')
    res=query_search(ch)
    es_summary(res)

    #in belowcode, we find all the docment index id, and sort the indexes, Then we compare these relevant indexes to all indexes in document
    #to create a boolean model.                      
    numberofhits1=[]
    for doc in res['hits']['hits']:
        numberofhits1.append(doc['_id'])

    for i in range(len(numberofhits1)):
      numberofhits1[i]=int(numberofhits1[i])

    numberofhits1.sort()
    orderedsearch=numberofhits1
    totallist=np.zeros(5001)
    totallist1=np.zeros(5001)
    for i in range(5000):
        for j in range(len(orderedsearch)):
            if orderedsearch[j] == i+1:
                totallist1[i+1]=1
            
    precision=0.0
    recall=0.0
    mapr(precision,recall)
    ch=input('Would you like to query the search engine? press y/n:')

