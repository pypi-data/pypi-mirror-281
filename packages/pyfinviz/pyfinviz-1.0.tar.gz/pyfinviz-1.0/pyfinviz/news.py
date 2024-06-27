import pandas as pd

from pyfinviz.utils import WebScraper
from pyfinviz.base_url import get_url


class News:

    @staticmethod
    def __table_to_df__(table):
        trs = table.find_all('tr', recursive=False)
        info = []

        for tr in trs:
            tds = tr.find_all('td')
            td_a = tds[len(tds)-1].find('a')
            if td_a is None:
                continue
            time = '' if len(tds) < 2 else tds[1].text
            info.append({'Time': time, 'Headline': td_a.text, 'URL': td_a['href']})

        return pd.DataFrame(info)

    def __init__(self):
        self.main_url = f'{get_url(path="news")}'[:-1]
        self.soup = WebScraper.get_soup(self.main_url)

        div_ = self.soup.find('div', class_='news').find('table')
        trs_ = div_.find_all('tr', recursive=False)
        main_tables = trs_[len(trs_)-1].find_all('table')

        self.news_df = News.__table_to_df__(main_tables[0])
        self.blogs_df = News.__table_to_df__(main_tables[1])
