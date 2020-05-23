import urllib.request
from bs4 import BeautifulSoup
import re


from history import History

class SeparatedPageParser:
    def __init__(self, url, baseURL):
        request = urllib.request.Request(url)
        self.baseURL = baseURL
        self.list_of_histories = []
        self.currentPage = None
        self.nextLinks = []
        try:
            response = urllib.request.urlopen(request)
            htmlBytes = response.read()
            self.htmlStr = htmlBytes.decode("utf8")
        except:
            print("Some problems with parsing")

        self.datePattern = re.compile('\d{1,2} \S+ \d{4}, \d{2}:\d{2}')
    def getListOfHistories(self):
        return self.list_of_histories

    def getNextParsingPage(self):
        try:
            return self.baseURL + self.nextLinks[0]
        except:
            return None


    def startParsing(self):
        soup = BeautifulSoup(self.htmlStr, "html.parser")

        for a in soup.find_all('div', class_='row'):
            for one_span in a.find_all('span', class_= "pagina"):
                t = one_span.find_all('a', href=True)
                if not t:
                    self.currentPage = one_span.getText()
                else:
                    if self.currentPage is not None:
                        self.nextLinks.append(t[0]['href'])

            # Identifier, data and tags
            for tags in a.find_all('div', class_='col-sm-6'):
                for links in tags.find_all('a', href=True):
                    if links['href'].startswith("/bytag"):
                        currentHistory.addTag(links.text)
                        continue
                    id = links['href'].split('/')[-1]
                    potentialText = links.text.strip()
                    currentHistory = History(id)
                    if self.datePattern.match(potentialText):
                        currentHistory.setHistoryTime(potentialText)
                        currentHistory.setURL(self.baseURL + links['href'])

            for tags in a.find_all('div', class_ ="col-xs-12", style="margin:0.5em 0;line-height:1.785em"):
                # This is text of post
                #print(tags.text)
                currentHistory.setHistory(tags.get_text().strip())
            for tags in a.find_all('div' , class_="col-xs-12", style='text-align:center'):
                #print(tags.b.prettify())
                currentHistory.setVotes(tags.b.get_text())
                self.list_of_histories.append(currentHistory)


class OnePageParse:
    def __init__(self, url, baseURL):
        request = urllib.request.Request(url)
        self.baseURL = baseURL
        self.list_of_histories = []
        self.currentPage = None
        self.nextLinks = []
        try:
            response = urllib.request.urlopen(request)
            htmlBytes = response.read()
            self.htmlStr = htmlBytes.decode("utf8")
        except:
            print("Some problems with parsing")

        self.datePattern = re.compile('\d{1,2} \S+ \d{4}, \d{2}:\d{2}')
    def getListOfHistories(self):
        return self.list_of_histories

    def getNextParsingPage(self):
        try:
            return self.baseURL + self.nextLinks[0]
        except:
            return None


    def startParsing(self):
        soup = BeautifulSoup(self.htmlStr, "html.parser")

        for a in soup.find_all('div', class_='row'):
            for one_span in a.find_all('span', class_= "pagina"):
                t = one_span.find_all('a', href=True)
                if not t:
                    self.currentPage = one_span.getText()
                else:
                    if self.currentPage is not None:
                        self.nextLinks.append(t[0]['href'])

            # Identifier, data and tags
            for tags in a.find_all('div', class_='col-xs-6'):
                for links in tags.find_all('a', href=True):
                    if links.text.strip().startswith('#'):
                        currentHistory = History(links.text.strip()[1:])
                        currentHistory.setURL(self.baseURL + links['href'])
                    elif self.datePattern.match(links.text.strip()):
                        currentHistory.setHistoryTime(links.text.strip())
                    if links['href'].startswith("/bytag"):
                        currentHistory.addTag(links.text)

            for tags in a.find_all('div', class_ ="col-xs-12", style="margin:0.5em 0;line-height:1.785em"):
                # This is text of post
                #print(tags.text)
                currentHistory.setHistory(tags.get_text().strip())
            for tags in a.find_all('div' , class_="col-xs-12", style='text-align:center'):
                #print(tags.b.prettify())
                currentHistory.setVotes(tags.b.get_text())
                self.list_of_histories.append(currentHistory)


def adultCollector(list_of_histories, historyChecking, baseURL):
    for oneHistory in historyChecking:
        text = oneHistory.historyText
        if oneHistory.historyText == '18+':
            print('Parsing separated page: {}'.format(oneHistory.historyURL))
            onePage = SeparatedPageParser(oneHistory.historyURL, baseURL)
            onePage.startParsing()
            tmpList = onePage.getListOfHistories()
            list_of_histories.append(tmpList[0])
            list_of_histories[-1].setAdultFlag(True)
        else:
            list_of_histories.append(oneHistory)