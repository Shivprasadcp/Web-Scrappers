from selenium import webdriver
import time
import numpy as np
import pandas as pd 
from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import urlparse


class Flipkart:
    def __init__(self, driver=r'"C:\Users\DELL\Downloads\WEB SCRAPING\chromedriver_win32_new"'):
        self.driver = webdriver.Chrome(driver)

    def scraping(self, req_url):
        """
        Scrapes any given website
        :param req_url: url of website to be scraped
        :return: html response of the website
        """
        self.driver.get(req_url)
        time.sleep(1)
        html = self.driver.page_source
        return html
    
    # Rest of the code remains the same...


    
    def scrape_main_page(self, url):
        """Scrape Flipkart page.

        Returns:
            pd.DataFrame: Dataframe containing flipkart products list
        """
        html = self.scraping(url)
        soup = BeautifulSoup(html, 'html.parser')
        a_section = soup.find_all('div', {'class':'_2kHMtA'}) 

        title = []
        price = []
        image= []
        partial_reference = []
        ratings = []

        for i in a_section:

            if i.find('a', {'class':'_1fQZEK'})==None:
                title.append(np.nan)
                partial_reference.append(np.nan)
            else :
                if i.find('a', {'class':'_1fQZEK'})['href']==None:
                    partial_reference.append(np.nan)
                else :
                    partial_reference.append(i.find('a', {'class':'_1fQZEK'})['href'])
                    j = i.find('a', {'class':'_1fQZEK'})
                    if j.find('div', {'class':'_4rR01T'})==None:
                        title.append(np.nan)
                    else :
                        title.append(j.find('div', {'class':'_4rR01T'}).text)

            if i.find('div', {'class':'_30jeq3 _1_WHN1'})==None:
                price.append(np.nan)
            else :
                price.append(i.find('div', {'class':'_30jeq3 _1_WHN1'}).text)

            if i.find('img', {'class':'_396cs4'})==None:
                image.append(np.nan)
            else :
                if i.find('img', {'class':'_396cs4'})['src']==None:
                    image.append(np.nan)
                else :
                    image.append(i.find('img', {'class':'_396cs4'})['src'])

            if i.find("div", {"class": "_3LWZlK"}) == None:
                ratings.append(np.nan)
            else:
                ratings.append(i.find("div", {"class": "_3LWZlK"}).text.strip())

        df=pd.DataFrame({'Product Title':title,'Price':price,'Image':image, 'Partial_url':partial_reference, 'Ratings': ratings})

        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + '://' + parsed_url.netloc
        df["complete url"] = base_url + df["Partial_url"]

        x = df.dropna()
        x.reset_index(inplace=True)

        #printing the result
        return x
    
    def scrape_product_details(self, x):
        dfs = []
        for url in x['complete url']:
            html = self.scraping(url)
            soup = BeautifulSoup(html, 'html.parser')
            try:
                title = soup.find('span', class_='B_NuCI').text
            except:
                title = np.nan
            try:
                price = soup.find('div', class_='_30jeq3 _16Jk6d').text
            except:
                price = np.nan
            try:
                available_offers = soup.find('div', class_='_3TT44I').text
            except:
                available_offers = np.nan
            try:
                highlights = soup.find('div', class_='_2cM9lP').text
            except:
                highlights = np.nan
            try:
                specifications = soup.find('div', class_='_3dtsli').text
            except:
                specifications = np.nan
            try:
                rating_reviews = soup.find('div', class_='col JOpGWq').text
            except:
                rating_reviews = np.nan
            data = {'Product Title': title, 'Price': price, 'Available Offers': available_offers, 
                    'Highlights': highlights, 'Specifications': specifications, 
                    'Rating & Reviews': rating_reviews, 'complete url': url}  # add 'Complete URL' column
            df_temp = pd.DataFrame(data, index=[0])
            dfs.append(df_temp)
        y = pd.concat(dfs, ignore_index=True)
        return y



    def merge_data(self, df1, df2):
        merged_df = pd.merge(df1, df2, on=['complete url'])
        return merged_df


    def extract(self, url):
        x=self.scrape_main_page(url)
        y = self.scrape_product_details(x)
        z = self.merge_data(x, y)
        z = z.drop(['Product Title_x', 'Price_y'], axis=1)
        return z
    
    
if __name__=='__main__':
    obj=Flipkart()
#     x= obj.scrape_main_page('https://www.flipkart.com/search?q=mobiles&otracker=AS_Query_HistoryAutoSuggest_5_0&otracker1=AS_Query_HistoryAutoSuggest_5_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=5&as-type=HISTORY')
#     y=obj.scrape_product_details(x)
#     z=obj.merge_data(x,y)
    z=obj.extract('https://www.flipkart.com/search?q=mobiles&otracker=AS_Query_HistoryAutoSuggest_5_0&otracker1=AS_Query_HistoryAutoSuggest_5_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=5&as-type=HISTORY&page=6')
    print(z) 

