 #------------------   setFiles  ---------------------------------------
def parseAlternatingLinesFile(file):     #-----------------------------
   # read a sequence of pairs of lines, e.g. text of webpage(s), name/URL
   sequenceA = []
   sequenceB = [] 
   fp = open(file, 'r')
   expectingA = True 
   for line in fp.readlines():
       if expectingA:
           sequenceA.append(line.rstrip())
           expectingA = False
       else:
           sequenceB.append(line.rstrip())
           expectingA = True
   fp.close()
   return sequenceA, sequenceB
 
 #------------------   printResults  ---------------------------------------

def valueOfSuggestion(result, position, targets):   #-----------------------------
    weight = [1.0, .5, .25]
    if result in targets:
        return weight[max(position, targets.index(result))]
    else:
        return 0

def scoreResults(results, targets):   #-----------------------------
    merits = [valueOfSuggestion(results[i], i, targets) for i in [0,1,2]]
    return sum(merits)

def scoreAllResults(queries, results, targets, descriptor):   #-----------------------------
    print ('\nScores for ' + descriptor)
    scores = [] 
    for q, r, t in zip(queries, results, targets):
       print ('for query: ' + q,)
       print (' results = ',)
       print (r,)
       print (' targets = ',)
       print (t,)
       s = scoreResults(r, t)
       print ('  score = %.3f' % s)
       scores.append(s)
    overallScore = np.mean(scores)
    print( 'all scores',)
    print (scores)
    print ('overall score of '+descriptor+' is %.3f' %overallScore)
    return overallScore

 
#------------------   tf-idf  ---------------------------------------
def tf(dictionary, inventory):
   tf_dict = dict()
   for word ,count in dictionary.items():
      tf_dict[word] = count/float(len(inventory))
   return tf_dict
   
def idf(archive):
   idf_dict = {}
   idf_dict = dict.fromkeys(archive.keys(),0)
   for word, val in archive.items():
       if val > 0:
          idf_dict[word] += 1

   for word, val in idf_dict.items():
      idf_dict[word] = np.log(len(archive) / float(val))
   return idf_dict

def tfidf(tfs,idfs):
   tfdif_dict = dict()
   for word, val in tfs.items():
      tfdif_dict[word] = val * idfs[word]
   return tfdif_dict

def tfidf_retrieve(queries, unigrams, archive):
   top3sets = []
   similarities = []
   for query in queries:
    for d in archive:
      w = d 
      w.update({query:1.0})
      tfwq = tf(w, query)
      tfwd = tf(w,d)
      idfw = idf(w)

      tfqq = tf(unigrams, query)
      idfq = idf(unigrams)

      tfdd = tf(unigrams, d)
      idfd = idf(d)

      vectForm = lambda l : [j for i,j in l.items()]
      sumOfAll = lambda l,k,p : np.sum([i*y*(z**2) for i,y,z in zip(l,k,p)])

      sqrtSumPow = lambda l,k : np.sqrt(np.sum([(x*y)**2 for x,y in zip(l,k)]))

      similarities.append( sumOfAll(vectForm(tfwq),vectForm(tfwd),vectForm(idfw)/ (sqrtSumPow(vectForm(tfqq),vectForm(idfq)) * sqrtSumPow(vectForm(tfdd),vectForm(idfd))) ) )

    #print similarities 
    top3indices = np.argsort(similarities)[0:3]
   #print "top three indices are "
   #print top3indices
    top3sets.append(top3indices)  
   return top3sets


#------------------   Word2Vect  ---------------------------------------
def wv_similarity(doc, query):
   '''retun the similarity of a document realted to the given query
      literaly  function 23.7'''
   vector_length = lambda l : np.sqrt(np.sum([i**2 for i in l]))
   return np.sum([np.dot(q,d) for q,d in zip(query,doc)]) \
   /np.dot(vector_length(query),vector_length(doc))

def wv_retrieve(queries, model, archive):
   top3sets = []
   for query in queries:
      try:
         q = [model.wv[word] for word in query.split()]
         #print( query)
      except KeyError:
         #print('{} not found in webages'.format(query))
         continue
      similarities = []
      for d in archive:
         similarities.append(wv_similarity([model.wv[word] for word in d.split()],q))
      #print similarities 
      top3indices = np.argsort(similarities)[0:3]
      #print "top three indices are "
      #print top3indices
      top3sets.append(top3indices)  
   return top3sets
 

#------------------   Unigram  ---------------------------------------
def computeSimilarity(dict1, dict2):   #-----------------------------
    # ad hoc and inefficient
    matchCount = 0
    for uni in dict1:
        if uni in dict2:
            #print ("match on " + uni)
            matchCount += 1 
    similarity = matchCount / float(len(dict2))
    #print ('similarity %.3f' % similarity)
    return similarity

def pruneUniqueNgrams(ngrams):        # ----------------------
    twoOrMore = {} 
    print ('before pruning: %d ngrams across all documents' % len(ngrams))
    for key in ngrams:
        if ngrams[key] > 1:
            twoOrMore[key] = ngrams[key]
    print ('after pruning: %d ngrams across all documents' % len(twoOrMore))
    return twoOrMore

def computeFeatures(text, unigramInventory):        #-----------------------------
    ''' catches the similarities between  "social" and "societal" etc. 
     but really should be replaced with something better'''
    unigrams = text.split()
    counts = {}
    for unigram in unigrams:
        if unigram in unigramInventory:
            if unigram in counts:
                counts[unigram] += 1
            else:
                counts[unigram] = 1        
    return counts

def retrieve(queries, unigramInventory, archive):      #-----------------------------
    # returns an array: for each query, the top 3 results found
    top3sets = [] 
    for query in queries:
        #print 'query is ' + query
        q = computeFeatures(query, unigramInventory)
        #print 'query features are '
        #print q
        similarities = [] 
        for d in archive:
           
            similarities.append(computeSimilarity(q, d))
        #print similarities 
        top3indices = np.argsort(similarities)[0:3]
        #print "top three indices are "
        #print top3indices
        top3sets.append(top3indices)  
    return top3sets

def findAllNgrams(contents):          # ----------------------
    unigrams = {}
    for text in contents:
        for uni in text.split():
            if uni in unigrams:
                unigrams[uni] += 1
            else:
                unigrams[uni] = 1
    return unigrams

def targetNumbers(targets, nameInventory):        # ----------------------
    # targets is a list of strings, each a sequence of names
    targetIDs = []
    for target in targets:
      threeNumbers = [] 
      for name in target.split():
          threeNumbers.append(nameInventory.index(name))
      targetIDs.append(threeNumbers)
    return targetIDs
   

# main ----------------------------------------------------
import sys, numpy as np
from  gensim.models import Word2Vec # used for generating the word vectors
from collections import Counter
import copy

print('......... irStub .........')
contents, names =  parseAlternatingLinesFile('../res/csFaculty.txt')
print ('read in pages for ',)
print (names)

unigramInventory = pruneUniqueNgrams(findAllNgrams(contents))
archive = [computeFeatures(line, unigramInventory) for line in contents]

queryFile = '../res/'

if len(sys.argv) >= 2 and (sys.argv[1] == 'yesThisReallyIsTheFinalRun'):
    queryFile += 'testQueries.txt'
else: 
    queryFile += 'trainingQueries.txt'
#file set up
queries, targets = parseAlternatingLinesFile(queryFile)
targetIDs = targetNumbers(targets, names)


# unigram
print ('='*20+ "unigrams"+'='*20)
results = retrieve(queries, unigramInventory, archive)
modelName = 'Unigrams '
scoreAllResults(queries, results, targetIDs, modelName + ' on ' + queryFile)


# word2vec
print ('='*20+ "word2vec and similatities"+'='*20)
w2vec_model = Word2Vec([ line.split() for line in contents],size = 64, min_count = 1)

results = wv_retrieve(queries,w2vec_model,contents)
modelName = 'Word2Vec '
scoreAllResults(queries, results, targetIDs, modelName + ' on ' + queryFile)


# tf-idf
print ('='*20+ "tf_idf"+'='*20)
results = tfidf_retrieve(queries,unigramInventory,archive)
modelName = 'tf-idf'
scoreAllResults(queries, results, targetIDs, modelName + ' on ' + queryFile)

