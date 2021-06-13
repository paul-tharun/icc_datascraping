# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker
from icc.models import db_connect, playersData, create_items_table


class IccPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_items_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        playerdata = playersData()
        playerdata.Name = item["Name"][0]
        playerdata.Country = item["Country"][0]
        playerdata.Type = item["Type"][0]
        playerdata.Date = item["Date"][0]
        playerdata.Rating = item["Rating"][0]

        try:
            session.add(playerdata)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item


## Todo Check for Duplicates

# class DuplicatesPipeline(object):
#     """[summary]
#     Checks for Duplicates
#     """
#     def __init__(self):
#         """
#         Initializes database connection and sessionmaker.
#         Creates tables.
#         """
#         engine = db_connect()
#         create_items_table(engine)
#         self.Session = sessionmaker(bind=engine)

#     def process_item(self, item, spider):
#         session = self.Session()
