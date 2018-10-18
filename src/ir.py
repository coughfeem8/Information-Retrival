
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

def retrieve(queries, trigramInventory, archive):      #-----------------------------
    # returns an array: for each query, the top 3 results found
    top3sets = [] 
    for query in queries:
        #print 'query is ' + query
        q = computeFeatures(query, trigramInventory)
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
        for uni in text:
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
    print ('overall score is %.3f' % overallScore)
    return overallScore
    

# main ----------------------------------------------------
import sys, numpy as np

print('......... irStub .........')
contents, names =  parseAlternatingLinesFile('../res/csFaculty.txt') 
print ('read in pages for ',)
print (names)
UnigramInventory = pruneUniqueNgrams(findAllNgrams(contents))
archive = [computeFeatures(line, trigramInventory) for line in contents]
queryFile = '../res/'

if len(sys.argv) >= 2 and (sys.argv[1] == 'yesThisReallyIsTheFinalRun'):
    queryFile += 'testQueries.txt'
else: 
    queryFile += 'trainingQueries.txt'

queries, targets = parseAlternatingLinesFile(queryFile)
targetIDs = targetNumbers(targets, names)
results = retrieve(queries, unigramInventory, archive)
modelName = 'silly character trigram model'
scoreAllResults(queries, results, targetIDs, modelName + ' on ' + queryFile)
