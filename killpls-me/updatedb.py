import time
import random
import sqlite3

from parsers import OnePageParse
from parsers import SeparatedPageParser
from parsers import adultCollector
from history import History

conn = sqlite3.connect('killmepls.db')
c = conn.cursor()

for row in c.execute("SELECT MAX(hID) FROM stories"):
    last_hID = row[0]
print(last_hID)

list_of_histories = []

currentURL = 'https://killpls.me'
baseURL = 'https://killpls.me'


main_page = OnePageParse(currentURL, baseURL)
main_page.startParsing()
historyChecking = main_page.getListOfHistories()
adultCollector(list_of_histories, historyChecking, baseURL)

nextURL = main_page.getNextParsingPage()
counter = 1

while nextURL:
    print('Next: {}'.format(nextURL))

    currentPage = OnePageParse(nextURL, baseURL)
    currentPage.startParsing()

    historyChecking = currentPage.getListOfHistories()
    adultCollector(list_of_histories, historyChecking, baseURL)

    if  last_hID in list(map(lambda x : x.historyID, list_of_histories)):
        print("We've faced history with ID = {}. Collection of histories stopped.".format(last_hID))
        break

    delay_sec = random.randint(1,5)
    print('Delay : {} seconds'.format(delay_sec))
    time.sleep(delay_sec)
    print('At iteration: {} we have {} histories'.format(counter, len(list_of_histories)))
    nextURL = currentPage.getNextParsingPage()
    counter += 1

sqlite_insert_with_param = """INSERT INTO 'stories'
                          ('hID', 'hdate', 'url', 'history', 'tags', 'votes', 'lastAccess', 'adult') 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""

for one_history in list_of_histories:
    data_tuple = (one_history.historyID,
                  one_history.historyTime,
                  one_history.historyURL,
                  one_history.historyText,
                  ' '.join(one_history.historyTags),
                  one_history.historyVotes,
                  one_history.lastAccessTime,
                  one_history.adultFlag)
    try:
        c.execute(sqlite_insert_with_param, data_tuple)
    except sqlite3.IntegrityError:
        print("Uniqueness violation: {}\t{}".format(data_tuple[0], data_tuple[2] ))

conn.commit()
conn.close()
