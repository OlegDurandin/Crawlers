import datetime

class History:
    def __init__(self, id):
        self.historyID = int(id)

        currentTime = datetime.datetime.now()
        self.lastAccessTime = currentTime.strftime("%m/%d/%Y, %H:%M:%S")
        self.historyTime = ''
        self.historyURL = ''
        self.historyTags = []
        self.historyText = ''
        self.historyVotes = 0
        self.adultFlag = False
    def setHistoryTime(self, hTime):
        self.historyTime = hTime
    def setURL(self, URL):
        self.historyURL = URL
    def addTag(self, tag):
        self.historyTags.append(tag)
    def setHistory(self, hText):
        self.historyText = hText
        if (self.historyText == '18+'):
            self.adultFlag = True
    def setAdultFlag(self, boolFlag):
        self.adultFlag = boolFlag
    def setVotes(self, hVotes):
        self.historyVotes = int(hVotes)