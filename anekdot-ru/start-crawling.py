from initselenium import selenium_initializer
from dbstruct import *
from datetime import datetime
from datetime import timedelta, date

from crawl_logic import parsing_by_date
from crawl_logic import process_one_anecdote

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

MAIN_PAGE = 'https://www.anekdot.ru/'
PREFIX = 'https://www.anekdot.ru/release/anekdot/day/'



if __name__ == "__main__":
    driver = selenium_initializer()
    driver.get(MAIN_PAGE)

    start_date = date(2020, month=4, day=1)
    end_date = date(2020, month=5, day=1)
    for single_date in daterange(start_date, end_date):
        date_postfix = single_date.strftime("%Y-%m-%d")
        current_URL = PREFIX + date_postfix
        print('Current date: {} {}'.format(date_postfix, current_URL))

        list_of_daily_anecs = parsing_by_date(driver, current_URL)
        print('We have {} anecdotes.'.format(len(list_of_daily_anecs)))
        for one_anecdote in list_of_daily_anecs:
            process_one_anecdote(one_anecdote)
        print('Insert into db for date {} complete'.format(date_postfix))





