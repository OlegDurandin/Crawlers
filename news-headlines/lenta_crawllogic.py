from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from dbstruct import LentaHeads, LentaNews

from initselenium import selenium_initializer

from datetime import datetime
from datetime import timedelta, date
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def extract_properties(one_news_block):
    time_and_date = one_news_block.find_element_by_class_name('g-date.item__date').text
    time_of_news, date_of_news = time_and_date.split(' — ')

    url_news = one_news_block.find_element_by_class_name('titles').find_element_by_tag_name('a').get_attribute('href')
    header_of_news = one_news_block.find_element_by_class_name('titles').find_element_by_tag_name('a').text

    return {
        'time': time_of_news,
        'date': date_of_news,
        'url': url_news,
        'header': header_of_news
    }


def process_one_lenta_header(one_news_block):
    transformed_data = one_news_block['date']
    eng_month_names = "january,february,march,april,may,june,july,august,september,october,november,december".split(',')
    rus_month_names = "января,февраля,марта,апреля,мая,июня,июля,августа,сентября,октября,ноября,декабря".split(',')
    for rus_name, eng_name in zip(rus_month_names, eng_month_names):
        transformed_data = transformed_data.lower().replace(rus_name, eng_name)

    t = datetime.strptime(one_news_block['time'], '%H:%M')

    headID, was_created = LentaHeads.get_or_create(
            date = datetime.strptime(transformed_data, '%d %B %Y'),
            time = datetime.strptime(one_news_block['time'], '%H:%M'),
            url = one_news_block['url'],
            header = one_news_block['header']
    )

    return headID, was_created


START_NEWS_DATE = 'https://lenta.ru/1999/08/31/'
if __name__ == "__main__":
    driver = selenium_initializer()
    driver.get(START_NEWS_DATE)

    start_date = date(1999, 9, 22)
    end_date = date(1999, 10, 1)
    delta = timedelta(days=1)

    while start_date <= end_date:
        current_day_news_headers = []
        URL = 'https://lenta.ru/{}'.format(start_date.strftime("%Y/%m/%d"))
        print('Day: {} parsing URL: {}'.format(start_date.strftime("%Y/%m/%d"), URL))
        driver.get(URL)
        news_headers = driver.find_elements_by_class_name('item.news.b-tabloid__topic_news')
        for one_news_block in news_headers:
            current_day_news_headers.append(extract_properties(one_news_block))
        passed = 0
        for one_news_block in current_day_news_headers:
            headID, was_created = process_one_lenta_header(one_news_block)
            if not was_created:
                passed += 1
        print('\t We have {} news headers, in db passed {} news'.format(len(current_day_news_headers),
                                                                        passed))
        start_date += delta

    driver.close()

