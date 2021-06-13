import scrapy
import datetime
import json
from scrapy.loader import ItemLoader
from icc.items import Player


class iccSpider(scrapy.Spider):
    name = "icc"

    def start_requests(self):
        urls = {
            "batting": "https://cricketapi-icc.pulselive.com/icc-ratings/ranked/players/odi/bat?pageSize=100&at=",
            "bowling": "https://cricketapi-icc.pulselive.com/icc-ratings/ranked/players/odi/bowl?pageSize=100&at=",
            "all-rounder": "https://cricketapi-icc.pulselive.com/icc-ratings/ranked/players/odi/allround?pageSize=20&at=",
        }
        start_date = datetime.date(2016, 6, 6)
        end_date = datetime.date(2021, 6, 6)
        delta = datetime.timedelta(days=1)
        while start_date <= end_date:
            for i in urls.keys():
                url = urls[i] + str(start_date)
                request = scrapy.Request(
                    url=url, callback=self.parse, cb_kwargs=dict(Type=i)
                )
                request.cb_kwargs["date"] = start_date
                yield request
            start_date += delta

    def parse(self, response, Type, date):
        self.logger.info("Parse function called on {}".format(response.url))
        data = json.loads(response.text)["content"]
        for obj in data:
            loader = ItemLoader(item=Player())
            player = {
                "Name": obj["player"]["fullName"],
                "Country": obj["player"]["nationality"]
                if "nationality" in obj["player"].keys()
                else "Unknown",
                "Type": Type,
                "Date": date,
                "Rating": obj["rating"],
            }

            loader.add_value(None, player)
            yield loader.load_item()
