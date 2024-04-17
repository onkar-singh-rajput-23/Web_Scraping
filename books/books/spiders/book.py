import scrapy
from pathlib import Path
from pymongo import MongoClient
from datetime import datetime, timezone


client = MongoClient("mongodb+srv://test:test12345678@mydatabase.inrnjd6.mongodb.net/")
db = client.scrapy


def insrttodb(page, title, rating, image, price, instock):
    collection = db[page]
    doc = {
        "title": title,
        "ratting": rating,
        "image": image,
        "price": price,
        "instock": instock,
        "date": datetime.now(timezone.utc),
    }
    inserted = collection.insert_one(doc)
    return inserted.inserted_id


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
        bookdetails = {}

        self.log(f"Saved file {filename}")
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3>a::text").get()
            # print(title)

            rating = card.css(".star-rating").attrib["class"].split(" ")[1]
            # print(rating)

            image = card.css(".image_container img")
            image = image.attrib["src"]
            # print(image.attrib["src"])

            price = card.css(".price_coclor::text").get()
            # print(price)

            avalibility = card.css(".availability")
            if len(avalibility.css(".icon-ok")) > 0:
                instock = True
            else:
                instock = False
            insrttodb(page, title, rating, image, price, instock)
