from tkinter import Tk, ttk
from scrapy.crawler import CrawlerProcess
from rank_tracker import RankTrackerSpider

root = Tk()
root.title("Rank Tracker")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

label = ttk.Label(frame, text="Search")
label.grid(row=0, column=0, padx=(0, 10))

keyword = ttk.Entry(root)
keyword.grid(row=0, column=1)


def run_spider():
    RankTrackerSpider.query = keyword.get()

    crawler = CrawlerProcess()
    crawler.crawl(RankTrackerSpider)

    crawler.start()


button = ttk.Button(frame, text="Run", command=run_spider)
button.grid(row=1, column=0, pady=10, columnspan=2)

root.mainloop()

