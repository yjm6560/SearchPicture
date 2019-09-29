from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from FilePath import FilePathGetter

class Crawler:
    def __init__(self):
        self.search_url = None
        self.file_path = None

    def getFilePath(self):
        return self.file_path
    def getSearchUrl(self):
        return self.base_url
    def setSearchUrl(self, url):
        self.search_url = url
    def setFilePath(self, path):
        self.file_path = path

if __name__ == "__main__":
    print("Not implemented")