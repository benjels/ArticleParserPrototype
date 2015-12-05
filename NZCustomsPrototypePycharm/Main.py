#this program is a quick test to check how to use wikipedia miner services to determine new zealandness
__author__ = 'user'
import requests
import json
import os
import time

ListOfNZArticleIDs = [4913064, 61978, 33804, 18660332, 628782, 628345, 127254, 171988, 86654, 171974]
#in order: New Zealand, Nelson, Wellington, Auckland, Christchurch, Dunedin, Waitangi, New Plymouth, Hamilton, Napier
#at the moment we will only deal with a list of relevant IDs that include the article for New Zealand and some well known New Zealand town's and cities as our relevant NZ related "senses"

def main():
    traverseFiles()


#traverses all of the files that we want to check the NZness of. This function pretty much does everything but defers to helper functions.
def traverseFiles():
    #TODO: GET THE FILE THAT WE WILL BE APPLYING THE REST OF THE ALGORITHM ON AND TAKE ONE LINE OUT OF IT WHICH REPRESENTS ONE ARTICLE
    fileStringsToCheck = []
    for root, dirs, files in os.walk("C:\!2015SCHOLARSHIPSTUFF\dummyNzTest"):
        for file in files:
            time.sleep(0.25)
            print (root + "\\" + file)
            eachArticlePathString = root + "\\" + file
            eachArticleJSONFile = open(eachArticlePathString, "r")
            fileText = eachArticleJSONFile.readline()
            articleJSONObj = json.loads(fileText)
            articleText = (articleJSONObj['fulltext'])

            #use the plain text of this article to do a "search" type wikipedia miner query
            with requests.Session() as session:
                truncatedArticleText = articleText[0:200]#we can only give the search service a very short string when we are using it through the web service (hopefully this doesn't apply when we use it locally
                print("the actual text that will be given to the search service is: \n" + truncatedArticleText)
                url = "http://wikipedia-miner.cms.waikato.ac.nz/services/search?query=" + truncatedArticleText + "&complex=true&responseFormat=json"
                print("making search service request...")
                result = session.get(url)
                responseJSONObj = json.loads(result.text)#Dunedin Auckland Wellington Nelson Napier Blenhiem Masterton Featherston Taupo Taranaki waiata tui kiwi London

                #iterate over each identified term in the text (e.g. "blue")
                likelyRelevantSenses = [] # a list that will hold the senses in this text that score well with weight/probablity. I.E. SENSES THAT ARE PROBABLY KEY TO THE OVERALL SEMANTIC MESSAGE OF THE ORIGINAL TEXT (AS JUDGED BY WIKIPEDIA MINER)
               #TODO so for some reason it cannot detect the labels key in the response that wikipedia miner is sending back to me. This could be because wikipedia miner is sending back like an error rather than a json string. maybe im ddosing it.
                print("this is the response: " + str(responseJSONObj))
                for eachIDedTermInfo in responseJSONObj['labels']:
                    print("----------------------------------------------------------------------------------------------------")
                    print("the term: \"" + eachIDedTermInfo.get('text') + "\" has the following sense information: ")
                    i = 0
                    #iterate over each identified "sense" of this term (e.g. "blue (color)". This is done in order of descending weight.
                    for eachSense in eachIDedTermInfo.get('senses'):
                        print("-----------------------------------------")
                        print("sense" + str(i) +": " + eachSense.get('title'))
                        print("weight: " + str(eachSense.get('weight')))
                        print("prior prob: " + str(eachSense.get('priorProbability')))
                        #check if this sense is deemed relevant
                        if eachSense.get('weight') >= 0.1 or eachSense.get('priorProbability') >= 0.1: #note that these values are really jsut place holders
                            likelyRelevantSenses.append(eachSense)
                        i += 1
            #compare this list to our list of NZ articles IDs and if we get matches, add to the list of matches with the appropriate NZProportionWeight
            sensesWhichMatchNZSense = [] #list of the senses that appear in both the established set of nz relevent senses and the set of senses from the supplied text that were deemed relevent.
            for eachArticleSense in likelyRelevantSenses: #TODO: this is obvs an inneficient way to do this and i will need to think about how to make these comparisons fast in the java implementation
                for eachNZSenseID in ListOfNZArticleIDs:
                    if eachArticleSense.get('id') == eachNZSenseID:
                        sensesWhichMatchNZSense.append(eachArticleSense)

            #at this point we should have all senses that were IDed in the supplied text that are also present in our collection of NZ related sense loaded into our list
            print(" \n \n \n ====== now printing out our final result senses (if any found) =======")
            for eachFoundRelevantSense in sensesWhichMatchNZSense:
                print(eachFoundRelevantSense)





if __name__ == "__main__":
    main()
    #jsonTest()
