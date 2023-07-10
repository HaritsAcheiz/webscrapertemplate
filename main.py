import csv
import os

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

    # write to csv function
    def to_csv(self, datas, filename):
        filepath = os.getcwd() + filename
        if os.path.exists(filepath):
            os.remove(filepath)
        for data in datas:
            with open(filename, 'a', encoding='utf-8') as f:
                headers = ['var1', 'var2', 'var3']
                writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=headers)
                if os.path.exists(filepath):
                    writer.writeheader()
                writer.writerow(data)

    # main function
    def main(self):
        # define targerted url
        url = 'https://www.google.com'

        # main program
        response = self.reg_fetch(url)
        datas = self.parse(response)
        print(datas)
        self.to_csv(datas, 'result.csv')

if __name__ == '__main__':
    s = Scraper()
    s.main()