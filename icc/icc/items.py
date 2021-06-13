# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Player(Item):
    """Player Container (dictionary-like object) for scraped data"""

    Name = Field()
    Country = Field()
    Type = Field()
    Date = Field()
    Rating = Field()
