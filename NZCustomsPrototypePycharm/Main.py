#this program is a quick test to check how to use wikipedia miner services to determine new zealandness
__author__ = 'user'
import requests
import json

ListOfNZArticleIDs = [4913064, 61978, 33804, 18660332, 628782, 628345, 127254, 171988, 86654, 171974]
#in order: New Zealand, Nelson, Wellington, Auckland, Christchurch, Dunedin, Waitangi, New Plymouth, Hamilton, Napier
#at the moment we will only deal with a list of relevant IDs that include the article for New Zealand and some well known New Zealand town's and cities as our relevant NZ related "senses"

def main():
    traverseFiles()


#traverses all of the files that we want to check the NZness of. This function pretty much does everything but defers to helper functions.
def traverseFiles():

    #for now just testing this on a single files but will use the os.walk() function to recursively explore some dir

    #convert each file to plain text with some stuff omitted (e.g. the json syntax and the article hash id etc)
    eachArticleJSONFile = open('C:\!2015SCHOLARSHIPSTUFF\dummyNzTest\[from_the_argus.]_new_zealand._wellington,_november_17..json', "r")
    fileText = eachArticleJSONFile.readline()
    articleJSONObj = json.loads(fileText)
    articleText = (articleJSONObj['fulltext'])

    #use the plain text of this article to do a "search" type wikipedia miner query
    with requests.Session() as session:
        url = "wikipedia-miner.cms.waikato.ac.nz/services/search?query=" + articleText + "&complex=true"
        print(url)
    #parse the result of our query and add all senses that scored over 0.3 in weight/probability to a list


    #compare this list to our list of NZ articles IDs and if we get matches, add to the list of matches with the appropriate NZProportionWeight




if __name__ == "__main__":
    main()
