import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import numpy as np
import pandas as pd
from urllib.parse import urlparse
from selenium import webdriver
import time
import numpy as np
import pandas as pd 
from bs4 import BeautifulSoup
import re


class TripAdvisor:
    def scrape_main_page(self,url):
        # opening the website using selenium
        driver = webdriver.Chrome()
        driver.get(url)

        # Retrieving the source code of the web page
        html = driver.page_source

        # Creating a BeautifulSoup object
        soup = BeautifulSoup(html, 'html.parser')

        # Extraction of Titles
        titles = soup.find_all('div', class_='XfVdV o AIbhI')

        # Extraction of Ratings
        ratings = soup.find_all('svg', class_='UctUV d H0 hzzSG')

        # Extraction of No. of Reviews
        No_of_reviews = soup.find_all('span', class_='biGQs _P pZUbB osNWb')

        # Extraction of Images
        images = soup.find_all('div', class_='yMdQy w')

        titles_list = []
        No_of_reviews_list = []
        images_list = []
        links_list = []

        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + '://' + parsed_url.netloc +  str('/')

        for title, rating, review, img in zip(titles, ratings, No_of_reviews, images):
            titles_list.append(title.text)

            if review != None:
                No_of_reviews_list.append(review.text)
            else:
                No_of_reviews_list.append("Not Avaliable")
            if img != None:
                images_list.append(img.find('img').get('src'))
            else:
                images_list.append("Not Avaliable")

        # Extracting the links to each attraction
        place_links = soup.find_all('div', class_='alPVI eNNhq PgLKC tnGGX')
        for link in place_links:
            href = link.find('a')['href']
            complete_link = base_url + href
            links_list.append(complete_link)

        # Storing the data in a Dataframe
        temp_df = pd.DataFrame({'Title': titles_list,
                                'No_of_reviews': No_of_reviews_list,
                                'Images': images_list,
                                'complete url': links_list})
        x = temp_df.dropna()

        #printing the result
        return x
    
 
    def scrape_place_data(self,x):
        # Create an empty list to store the scraped data
        data_list = []

        # Iterate over the URLs
        for url in x['complete url']:
            # Opening the website using selenium
            driver = webdriver.Chrome()
            driver.get(url)

            # Retrieving the source code of the web page
            html = driver.page_source

            # Creating a BeautifulSoup object 
            soup = BeautifulSoup(html, 'html.parser')

            title = soup.find('h1',class_='biGQs _P fiohW eIegw')
            if (title !=None):
                title = title.text
            else :
                title = np.nan

            popular_for = soup.find('div',class_='fIrGe _T bgMZj')
            if (popular_for !=None):
                popular_for = popular_for.text.replace('Points of Interest & Landmarks','')
            else:
                popular_for = np.nan

            timing = soup.find('span',class_='EFKKt')
            if (timing !=None):
                timing = timing.text
            else:
                timing = np.nan

            about = soup.find('div',class_='_d MJ')
            if (about !=None):
                about = about.text.replace('Read more','')
            else:
                about = np.nan

            images = soup.find_all('div',class_='Kxegy _R w _Z GA')
            if (images!=None):
                image_urls = []
                for image in images:
                    img_tag = image.find('img')
                    img_url = img_tag['src']
                    index = img_url.find('?')
                    new_img_url = img_url[:index] + '?w=500&h=-1&s=1'
                    image_urls.append(new_img_url)
            else :
                image_urls = np.nan

            add = soup.find_all("div",class_="MJ")
            if (add!=None):
                try:
                    address = add[1]
                    if (address !=None):
                        address = address.text.replace('Address','')
                    else:
                        address = np.nan
                except IndexError:
                    address = np.nan
            else :
                address = np.nan


            recommended_list = soup.find_all('div', class_='keSJi FGwzt ukgoS')
            if (recommended_list !=None):
                recommended_places = []
                for i in range(len(recommended_list)):
                    recommended_places.append(recommended_list[i].text)
            else:
                recommended_places = np.nan

            # Append the scraped data as a dictionary to the list
            data_list.append({'Title': title, 'Popular for': popular_for, 'Timing': timing, 'About': about, 'Image URLs': image_urls, 'Address': address, 'Recommended Places': recommended_places, 'complete url': url})

            # Close the selenium driver
            driver.close()

        # Create a new dataframe from the list of dictionaries
        y = pd.DataFrame(data_list)

        # Return the new dataframe
        return y
    
    def merge_data(self, df1, df2):
        merged_df = pd.merge(df1, df2, on=['complete url'])
        return merged_df
    
    def extract(self, url):
        x=self.scrape_main_page(url)
        y = self.scrape_place_data(x)
        z = self.merge_data(x, y)
        return z

if __name__ == '__main__':
    # Call the generate_report() function on the DataFrame
    obj =TripAdvisor()
    z = obj.extract('https://www.tripadvisor.com/Attractions-g6-Activities-oa0-Africa.html')
    print(z)