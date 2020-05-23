import time
import random
import sqlite3

from parsers import OnePageParse
from parsers import SeparatedPageParser
from parsers import adultCollector
from history import History

COUNT_OF_PAGES = 1000

conn = sqlite3.connect('killmepls.db')
c = conn.cursor()

# Create table
try:
    c.execute('''CREATE TABLE stories
                 (  hID INTEGER PRIMARY KEY,
                    hdate text,  
                    url text,
                    history text,
                    tags text,
                    votes int,
                    lastAccess text, 
                    adult BOOL)''')
except sqlite3.OperationalError:
    print('Table already exists.. passed')

list_of_histories = []

#currentURL = 'https://killpls.me/'
currentURL = 'https://killpls.me/page/243'
baseURL = 'https://killpls.me'


main_page = OnePageParse(currentURL, baseURL)
main_page.startParsing()
historyChecking = main_page.getListOfHistories()
adultCollector(list_of_histories, historyChecking)
nextURL = main_page.getNextParsingPage()
counter = 1

while nextURL and (counter < COUNT_OF_PAGES):
    print('Next: {}'.format(nextURL))

    currentPage = OnePageParse(nextURL, baseURL)
    currentPage.startParsing()

    historyChecking = currentPage.getListOfHistories()
    adultCollector(list_of_histories, historyChecking)

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


# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
