import pandas as pd
from asx_tracker.database.database import Database

class Scraper():

    # Static variables

    _COL_ETP_TICKER = 'ASX Code'
    _COL_ETP_MGMT_PCT = 'Management Cost %'
    _COL_ETP_NAME = 'Exposure'
    _COL_ETP_TYPE = 'Type'
    _COL_COM_TICKER = 'ASX code'
    _COL_COM_NAME = 'Company name'

    _URL_COM = 'https://www2.asx.com.au/markets/trade-our-cash-market/directory'
    _URL_ETP = 'https://www2.asx.com.au/markets/trade-our-cash-market/asx-investment-products-directory/etps'
    #_URL_COM = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv' # This is outdated


    # Scrape all
    @staticmethod
    def scrape_all_listings(comp_url):
        return pd.concat([Scraper.scrape_etfs(), Scraper.scrape_companies(comp_url)])


    # Scrape ETFs

    @staticmethod
    def scrape_etfs():
        dfs = pd.read_html(Scraper._URL_ETP, header=0)
        df = pd.concat([df[[Scraper._COL_ETP_TICKER,Scraper._COL_ETP_NAME,Scraper._COL_ETP_MGMT_PCT]][df[Scraper._COL_ETP_TYPE] == 'ETF'] for df in dfs], axis=0)
        df.rename(columns={Scraper._COL_ETP_TICKER: Database._COL_TICKER, Scraper._COL_ETP_NAME: Database._COL_NAME, Scraper._COL_ETP_MGMT_PCT: Database._COL_MGMT_PCT}, inplace=True)
        df[Database._COL_MGMT_PCT] *= 100
        df[Database._COL_MGMT_PCT] = df[Database._COL_MGMT_PCT].astype(int)
        return df.groupby(Database._COL_TICKER, as_index=False).max()


    # Scrape companies

    @staticmethod
    def scrape_companies(url):
        df = pd.read_csv(url, header=0)[[Scraper._COL_COM_TICKER, Scraper._COL_COM_NAME]]
        df.rename(columns={Scraper._COL_COM_TICKER: Database._COL_TICKER, Scraper._COL_COM_NAME: Database._COL_NAME}, inplace=True)
        df[Database._COL_NAME] = df[Database._COL_NAME].fillna('')
        df[Database._COL_MGMT_PCT] = 0
        return df


    # Scrape daily

    @staticmethod
    def scrape_daily():
        raise NotImplementedError()


    # Scrape intraday

    @staticmethod
    def scrape_intraday():
        raise NotImplementedError()