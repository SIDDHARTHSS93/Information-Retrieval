import urllib
from urllib import request
from bs4 import BeautifulSoup
from nltk import word_tokenize,re,pos_tag
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.tag import StanfordNERTagger
import os
import pandas as pd
import math
path="C:/Program Files/Java/jdk1.8.0_201/bin/java.exe"
os.environ['JAVAHOME']=path



def get_output(urlx):
    response=request.urlopen(urlx)
    rw=str(response.read().decode('utf-8'))
    soup=BeautifulSoup(rw,"html.parser")
    # Removing script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    #Finding meta tags
    meta = soup.find_all('meta')
    rel3 = ''
    for tag in meta:
        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description', 'keywords']:
            rel3 += tag.attrs['content']
            rel3 += '\n'
    # get plain text
    text_soup = soup.get_text()

    # Removing leading and trailing spaces
    lines = (line.strip() for line in text_soup.splitlines())
    # Breaking headlines into a line
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Removing blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    rel3 += text
    return rel3

def pre_processing(rel3):
    #Removing punctuations
    rel3=re.sub('[^a-zA-Z0-9_\.]',' ',rel3)

    #Lemmatization
    lem=WordNetLemmatizer()
    rel3=[lem.lemmatize(i,pos='v') for i in rel3]
    rel3=[lem.lemmatize(i,pos='n') for i in rel3]
    rel3=[lem.lemmatize(i,pos='a') for i in rel3]
    rel3=''.join(rel3)
    
    #Tokenization
    tokens = nltk.word_tokenize(rel3)
    return tokens

def pos_tag(text):
    tagged_words = nltk.pos_tag(text)
    return tagged_words

def NER_tagger(text):
    st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz','stanford-ner.jar') 
    result=st.tag(text)
    ner = ''
    for i in result:
        if i[1] in ('PERSON','ORGANIZATION','LOCATION'):
            ner += i[0]+' '+i[1]+'\n'
    return ner

file_url = open('URLs.txt','r')
count_of_url = 0
for url in file_url.readlines():

    #Extracting data from the url and writing into file
    plain_text = get_output(url)
    file_name = 'HTML_parsing'+str(count_of_url)+'.txt'
    file = open(file_name,'w')
    file.write(plain_text)
    file.close()

    #Pre-processing the text and writing output into a file
    file_name = 'pre_processing'+str(count_of_url)+'.txt'
    file = open(file_name,'w')
    pre_processed_text = pre_processing(plain_text)
    for word in pre_processed_text:
        file.write(word)
        file.write('\n')
    file.close()

    #POS tagging and writing into output into a file
    file_name = 'POS_tagging'+str(count_of_url)+'.txt'
    file = open(file_name,'w')
    tags = pos_tag(pre_processed_text)
    for i in tags:
        file.write(i[0]+' - '+i[1]+'\n')
    file.close()

    #NER tagging with the help of Stanford NER tagger
    NER_tagged_words = NER_tagger(pre_processed_text)
    file_name = 'NER_tagging'+str(count_of_url)+'.txt'
    file = open(file_name,'w')
    file.write(NER_tagged_words)
    file.close()
    
    count_of_url += 1
    
def get_url(urls):
    response=request.urlopen(urls)
    rw=str(response.read().decode('utf-8'))
    soup=BeautifulSoup(rw,"html.parser")
    # Removing script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    meta = soup.find_all('meta')
    rel3 = ''
    for tag in meta:
        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description', 'keywords']:
            rel3 += tag.attrs['content']
            rel3 += '\n'

    # get plain text
    text_soup = soup.get_text()

    # Removing leading and trailing spaces
    lines = (line.strip() for line in text_soup.splitlines())
    # Breaking headlines into a line
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Removing blank lines
    text_chunk = '\n'.join(chunk for chunk in chunks if chunk)
    rel3 += text_chunk

    rel3=re.sub('[^a-zA-Z0-9_\.]',' ',rel3)

    #Lemmatization
    lem=WordNetLemmatizer()
    rel3=[lem.lemmatize(i,pos='v') for i in rel3]
    rel3=[lem.lemmatize(i,pos='n') for i in rel3]
    rel3=[lem.lemmatize(i,pos='a') for i in rel3]
    rel3=''.join(rel3)

    #print(rel3)

    #Tokenization
    rel3=nltk.word_tokenize(rel3)

    return rel3
def bigrams(relx):
    bigramslist=[]
    bigramslist=list(nltk.bigrams(relx))
    return bigramslist
#def termFrequency(rel):

url3 = "https://www.essex.ac.uk/departments/computer-science-and-electronic-engineering"

rel3 = get_url(url3)

url = "http://csee.essex.ac.uk/staff/udo/index.html"
rel = get_url(url)

rel2=bigrams(rel3)

#Getting Phrases from URL
rel4=bigrams(rel)
#print(rel4)



def computeTFDict(text):
    #Counts the number of times the word appears in text
    TFDict = {}
    for word in text:
        if word in TFDict:
            TFDict[word] += 1
        else:
            TFDict[word] = 1
    #Computes tf for each word           
    for word in TFDict:
        TFDict[word] = TFDict[word] / len(text)
    return TFDict


x = computeTFDict(rel3)
x2=x


y = computeTFDict(rel)


x1 = computeTFDict(rel2)
x3=x1

y1 = computeTFDict(rel4)
z=x.update(y)



z1=x1.update(y1)

def computeCountDict(x,x1):
    countDict = {}

    for word in x:
        if word not in x1 and word not in countDict.keys():
            countDict[word]=1

    for word in x1:
        if word not in countDict.keys():
            countDict[word]=1
        if word in x and countDict[word]==1:
            countDict[word]=2


    return countDict

#Stores the review count dictionary
countDict = computeCountDict(rel3,rel)

countDictbi = computeCountDict(rel2,rel4)

def computeIDFDict(countDict):
    idfDict = {}
    for word in countDict:
        idfDict[word] = math.log(2 / countDict[word])
    return idfDict
  
#Stores the idf dictionary
idfDict = computeIDFDict(countDict)
#print(idfDict)
idfDictbi = computeIDFDict(countDictbi)


def computeTFIDFDict(TFDict,idfDict):
    TFIDFDict = {}
    #For each word in the review, we multiply its tf and its idf.
    for word in TFDict.keys():
        TFIDFDict[word] = TFDict[word] * idfDict[word]
    return TFIDFDict

#Stores the TF-IDF dictionaries
tfidfDict = computeTFIDFDict(x,idfDict)

tfidfDictbi = computeTFIDFDict(x1,idfDictbi)
#Sorting and comparion of the index table with URL data
formattedTFIDF=sorted(tfidfDict.items(),key= lambda t:t[1],reverse=True)
formattedTFIDFPhrase=sorted(tfidfDictbi.items(),key= lambda t:t[1],reverse=True)


print("After Indexing Keywords for,"+url3+'We have:')
count=0
count2=0
count3=0
count4=0
word1=''
word2=''
word3=''
word4=''
kp = open('Keywords and phrases.txt','w')
kp.write("After Indexing Keywords for,"+url3+'We have:\n\n')
kp.write('Index\tKeywords\n')
print('Index\tKeyWord\n')
for i in range(len(formattedTFIDF)):
    for word in x2:
        if formattedTFIDF[i][0]==word and formattedTFIDF[i][1]!=0.0:
            
            count+=1
            word1=str(count)+'\t'+word+'\t\n'
            kp.write(word1)
            print(count,'\t',word,'\t',end='\n')

kp.close()
print("\n\nAfter Indexing Keywords for,",url,'We have:')
kp = open('Keywords and phrases.txt','a')
kp.write("After Indexing Keywords for,"+url+'We have:\n\n')
kp.write('Index\tKeyWord\n')
print('\nIndex\tKeyWord')
for i in range(len(formattedTFIDF)):
    for word in y:
        if formattedTFIDF[i][0]==word and formattedTFIDF[i][1]!=0.0:
            
            count2+=1
            word2=str(count2)+'\t'+word+'\t'+'\n'
            kp.write(word2)
            print(count2-1,'\t',word,'\t',end='\n')
    
kp.close()
kp = open('Keywords and phrases.txt','a')
kp.write("After Indexing Phrases for,"+url3+'We have:\n\n')
kp.write('Index\tPhrases\n')
print("After Indexing phrases for,",url3,'We have:')
count=0
print('\nIndex\tPhrase')
for i in range(len(formattedTFIDFPhrase)):
    for word in x3:
        if formattedTFIDFPhrase[i][0]==word and formattedTFIDFPhrase[i][1]!=0.0:
            
            count3+=1
            word3=str(count3)+'\t'+' '.join(word)+'\t'+'\n'
            kp.write(word3)
            print(count3,'\t',' '.join(word),'\t',end='\n')

print("\n\nAfter Indexing phrases for,",url,'We have:')
count=0
kp = open('Keywords and phrases.txt','a')
kp.write("After Indexing Keywords for,"+url+'We have:\n\n')
kp.write('Index\tPhrases\n')
print('\nIndex\tPhrase')

for i in range(len(formattedTFIDF)):
    for word in y1:
        if formattedTFIDFPhrase[i][0]==word and formattedTFIDFPhrase[i][1]!=0.0:
            
            count4+=1
            word4=str(count4)+'\t'+' '.join(word)+'\t'+'\n'
            kp.write(word4)

            print(count4,'\t',' '.join(word),'\t',end='\n')

kp.close()

   
file_url.close()
