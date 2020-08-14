from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from dbstruct import Anecdot, Tags, TagsAnecdot, Authors

from datetime import datetime
from datetime import timedelta, date
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def parsing_by_date(driver, date_url_format):
    driver.get(date_url_format)
    anecdots_by_day = []

    next_page = ''

    while True:
        anecdots_elements = driver.find_elements_by_class_name('topicbox')
        current_date = anecdots_elements[0].find_element_by_class_name('subdate').get_attribute('innerHTML')
        for one_anec_element in anecdots_elements[1:]:
            res = parse_one_anecdote(one_anec_element)
            if res:
                res['date'] = current_date
                anecdots_by_day.append(res)
        try:
            if driver.find_element_by_class_name('pageslist').find_elements_by_tag_name('a')[-1].get_attribute(
                    'text') == 'след. →':
                next_page = driver.find_element_by_class_name('pageslist').find_elements_by_tag_name('a')[
                    -1].get_attribute('href')
                print('Go to next page: {}'.format(next_page))
                driver.get(next_page)
            else:
                break
        except NoSuchElementException:
            break
    return anecdots_by_day


def parse_one_anecdote(anecdote_element):
    res = {}
    try:
        res['id'] = anecdote_element.get_attribute('data-id')
        res['text'] = anecdote_element.find_element_by_class_name('text').text
    except NoSuchElementException:
        return None

    res['tags'] = []
    try:
        for one_tag in anecdote_element.find_element_by_class_name('tags').find_elements_by_tag_name('a'):
            res['tags'].append((one_tag.get_attribute('href'), one_tag.get_attribute('text')))
    except NoSuchElementException:
        pass

    try:
        positive_votes = anecdote_element.find_element_by_class_name('votingbox').find_element_by_class_name(
            "vote.p").get_attribute('title')
        res['positive'] = int(''.join(c for c in positive_votes if c.isdigit()))
        negative_votes = anecdote_element.find_element_by_class_name('votingbox').find_element_by_class_name(
            "vote.m").get_attribute('title')
        res['negative'] = int(''.join(c for c in negative_votes if c.isdigit()))
    except NoSuchElementException:
        res['negative'] = None
        res['positive'] = None

    res['url'] = anecdote_element.find_element_by_class_name('votingbox').find_element_by_tag_name('a').get_attribute(
        'href')
    res['discussion_count'] = anecdote_element.find_element_by_class_name('votingbox').find_element_by_tag_name(
        'a').get_attribute('data-com')

    try:
        res['author'] = (
            anecdote_element.find_element_by_class_name('auth').get_attribute('href'),
            anecdote_element.find_element_by_class_name('auth').get_attribute('text'),
        )
    except NoSuchElementException:
        res['author'] = None

    return res


def process_one_anecdote(one_anecdote):
    if one_anecdote['author'] is not None:
        authorID, was_created = Authors.get_or_create(
            authorURL=one_anecdote['author'][0],
            authorName=one_anecdote['author'][1])
    else:
        authorID = None
    current_anecdote, was_created = Anecdot.get_or_create(
        anecdotID=one_anecdote['id'],
        text=one_anecdote['text'],
        positive=one_anecdote['positive'],
        negative=one_anecdote['negative'],
        url=one_anecdote['url'],
        authorID=authorID,
        date=datetime.strptime(one_anecdote['date'], '%d.%m.%Y')
    )

    if was_created:
        for one_tag in one_anecdote['tags']:
            tag_row, tag_was_added = Tags.get_or_create(
                url=one_tag[0],
                name=one_tag[1])
            TagsAnecdot.create(anecdotID=current_anecdote,
                               tagID=tag_row)



