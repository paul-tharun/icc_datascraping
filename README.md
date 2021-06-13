# icc_datascraping
To run the scraper and the dashboard. Clone the repo and in the icc/icc folder
1. Add the postgresql database credentials and database name in settings.py and webapp.py
2. run
```
pip install -r requirements.txt
scrapy crawl icc
streamlit run webapp.py
```
