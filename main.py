import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import asyncio

# class to store scraped data
@dataclass
class Item:
    # define instance variable
    var1: str
    var2: str
    var3: str

# class to scrape data
@dataclass
class Scraper:
    # define instance variable
    ivar1: str = None
    ivar2: str = None

    # define function
    # fetch regular function
    def reg_fetch(self, url):
        # define headers
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
        }

        # define proxy

        # get request
        with httpx.Client(headers=headers) as client:
            response = client.get(url)

        return response

    # parse function
    def parse(self, response):
        # parse html
        tree = HTMLParser(response.text)

        # select element
        data1 = tree.css_first('title').text()
        data2 = tree.css_first('a').text()
        if tree.css_first('p'):
            data3 = tree.css_first('p').text()
        else:
            data3 = None

        # Conver result into dict form
        item = Item(var1=data1, var2=data2, var3=data3)

        return asdict(item)

    # main function
    def main(self):
        # define targerted url
        url = 'https://www.google.com'

        # main program
        response = self.reg_fetch(url)
        result = self.parse(response)
        print(result)

if __name__ == '__main__':
    s = Scraper()
    s.main()