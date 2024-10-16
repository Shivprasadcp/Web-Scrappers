from selenium import webdriver
import time
import numpy as np
import pandas as pd 
from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import urlparse


class Amazon:
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
    
    def scrape_main_page(self, url):
        """Scrape Amazon page.

        Returns:
            pd.DataFrame: Dataframe containing amazon products list
        """
        html = self.scraping(url)
        soup = BeautifulSoup(html, 'html.parser')
        a_section = soup.find_all('div', {'class':'sg-row'})
        title = []
        price = []
        image= []
        partial_reference = []
        ratings = []
        for i in a_section:

            if i.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})==None:
                title.append(np.nan)
                partial_reference.append(np.nan)
            else :
                if i.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']==None:
                    partial_reference.append(np.nan)
                else :
                    partial_reference.append(i.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href'])
                    j = i.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
                    if j.find('span', {'class':'a-size-medium a-color-base a-text-normal'})==None:
                        title.append(np.nan)
                    else :
                        title.append(j.find('span', {'class':'a-size-medium a-color-base a-text-normal'}).text)


            if i.find('span', {'class':'a-offscreen'})==None:
                price.append(np.nan)
            else :

                price.append(i.find('span', {'class':'a-offscreen'}).text)


            if i.find('img', {'class':'s-image'})==None:
                image.append(np.nan)
            else :
                if i.find('img', {'class':'s-image'})['src']==None:
                    image.append(np.nan)
                else :
                    image.append(i.find('img', {'class':'s-image'})['src'])


            if i.find('span', {'class':'a-icon-alt'})==None:
                ratings.append(np.nan)
            else:
                rating_str = i.find('span', {'class':'a-icon-alt'}).text
                match = re.search(r'([\d\.]+)', rating_str)
                if match:
                    ratings.append(float(match.group(1)))
                else:
                    ratings.append(np.nan)


        data = pd.DataFrame({'Product Title':title,'Price':price,'Image':image, 'Partial_url':partial_reference, 'Rating': ratings})
        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + '://' + parsed_url.netloc
        data["complete url"] = base_url + data["Partial_url"]
        x = data.dropna(axis='rows')
    
        return x
            


    
    def scrape_product_details(self,x):
        all_data = []
        for url in x['complete url']:
            

            html = self.scraping(url)
            soup = BeautifulSoup(html, 'html.parser')

            title = soup.find('span', {'id': 'productTitle'})
            if title is not None:
                title = title.text.strip()
            else:
                title = 'nan'

            price = soup.find('div', {'id': 'corePrice_desktop'})
            if price is not None:
                price = price.text.replace('\n', '').replace('Price:', '')

                # Extract the price from the string using regex
                price_match = re.search('\$(\d+\.\d+)', price)
                if price_match:
                    price = price_match.group(1)
                else:
                    price = 'nan'
            else:
                price = 'nan'

            features = soup.find('div', {'id': 'poExpander'})
            if features is not None:
                features = features.text.replace('\n', '')
            else:
                features = 'nan'

            description = soup.find('div', {'id': 'productDescription'})
            if description is not None:
                description = description.text.strip()
            else:
                description = 'nan'

            info = soup.find('div', {'id': 'prodDetails'})
            if info is not None:
                info = info.text.replace('\n', ' ')
            else:
                info = 'nan'

            similar_items = soup.find('div', {'id': 'HLCXComparisonWidget_feature_div'})
            if similar_items is not None:
                similar_items = similar_items.text.strip()
            else:
                similar_items = 'nan'

            reviews = soup.find('div', {'id': 'cm-cr-dp-review-list'})
            if reviews is not None:
                reviews = reviews.text.strip()
            else:
                reviews = 'nan'

            # Create a dictionary to store the scraped data
            data = {
                'Product Title': [title],
                'Product Features': [features],
                'Product Description': [description],
                'Product Information': [info],
                'Similar Products': [similar_items],
                'Product Reviews': [reviews]
            }

            # Create a pandas dataframe from the dictionary and append it to the list of data
            df_product = pd.DataFrame(data)
            all_data.append(df_product)



        # Concatenate all the dataframes into a single dataframe and return it
        df_final = pd.concat(all_data)
        return df_final
    
    

    def merge_data(self, df1, df2):
        merged_df = pd.merge(df1, df2, on=['Product Title'])
        return merged_df


    def extract(self, url):
        x=self.scrape_main_page(url)
        y = self.scrape_product_details(x)
        z = self.merge_data(x, y)
        return z
    
if __name__=='__main__':
    obj=Amazon()
    #unclean_df= obj.scrape_main_page('https://www.amazon.com/s?k=realme&ref=nb_sb_noss_1')
#     x=obj.scrape_main_page('https://www.amazon.com/s?k=realme&ref=nb_sb_noss_1') 
#     y= obj.scrape_product_details(x)
#     z = obj.merge_data(x, y)
    z=obj.extract('https://www.amazon.com/s?k=realme&ref=nb_sb_noss_1')
    print(z)

  