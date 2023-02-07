import scrapy
import json
from datetime import date


class RankTrackerSpider(scrapy.Spider):
    name = "rank_tracker"
    query = 'python for beginners'

    def __init__(self, query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base_url = "https://www.amazon.com"
        self.search_url = "https://www.amazon.com/s?k={query}"

        self.rank = None
        self.page_number = 1
        self.query = query if query else self.query

        print("[ query ]: ", self.query)

        self.start_urls = [self.search_url.format(
            query=self.query.replace(' ', '+')
        )]

    def parse(self, response):
        # title = 'Python 3.10: A Complete Guide Book To Python Programming For Beginners'
        title = 'Learn to Code by Solving Problems: A Python Programming Primer'

        search_results = response.css('div.s-result-item h2 > a > span::text').getall()

        if title in search_results:
            page_position = search_results.index(title) + 1
            self.rank = ((self.page_number - 1) * 48) + page_position
        else:
            next_button = response.css('a.s-pagination-next')
            if next_button:
                self.page_number += 1
                yield scrapy.Request(
                    self.base_url + next_button.attrib['href']
                )
            else:
                self.rank = "Not Found!"

        self.export()

    def export(self):
        today = date.today().strftime('%d-%m-%Y')

        with open("product_rank.json") as file:
            dt = json.load(file)

        if self.query in dt:
            dt[self.query][today] = self.rank
        else:
            dt[self.query] = {
                today: self.rank
            }

        with open('product_rank.json', 'w') as file:
            json.dump(dt, file)
