import sys
import mediacloud
import datetime
import csv
import logging

#basic logging

logging.basicConfig(level=logging.DEBUG)
logging.info("Calculating election counts!")

def ElectionCount(name):
    
    '''name is a string representing the word we want to search. Function returns the number of times a word appears in between selected dates'''
    
    mc = mediacloud.api.MediaCloud('809729c417734ad84451ecd3b1a0c8553c0dc84b6d23fd3afe30835c2ff42ad3') #replace with your actual API Key
    
    with open('electionlogging.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Success! API Connection has been made'])
        
        results = mc.sentenceCount('( name )', '+publish_date:[2016-01-01T00:00:00Z TO 2017-01-01T00:00:00Z} AND +tags_id_media:1')
        
        variable = str(results['count'])

        filewriter.writerow(variable)

    print (results['count'])

    return results['count']

ElectionCount ('Trump')



