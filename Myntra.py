from selenium import webdriver
import time
import numpy as np
import pandas as pd 
from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import urlparse

class Myntra:
    def __init__(self, browser_path='C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe', driver=r'C:\Users\DELL\Downloads\WEB SCRAPING\chromedriver_win32_new'):
        self.path = browser_path
        self.option = webdriver.ChromeOptions()
        # Remove the 'headless' option
        self.option.binary_location = self.path
        self.driver = webdriver.Chrome(driver, options=self.option)

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
    
    # ...

    def scrape_main_page(self, url):
                """Scrape Myntra page.

                Returns:
                    pd.DataFrame: Dataframe containing Myntra products list
                """
                # Open the page in the browser
                driver = webdriver.Chrome()
                driver.get(url)

                # Scroll down to the bottom of the page to load all products
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                # Get the HTML source code of the page
                html = driver.page_source

                # Use Beautiful Soup to parse the HTML and extract the product information
                soup = BeautifulSoup(html, 'html.parser')
                products = soup.find_all('li', {'class': 'product-base'})

                title = []
                brand = []
                discounted_price = []
                original_price = []
                discount_percentage = []
                image = []
                partial_reference = []
                rating = []

                for product in products:
                    # Extract the product information
                    name = product.find('h3', {'class': 'product-brand'})
                    if name is not None:
                        brand.append(name.text.strip())
                    else:
                        brand.append(np.nan)

                    price = product.find('span', {'class': 'product-discountedPrice'})
                    if price is not None:
                        discounted_price.append(price.text.strip())
                    else:
                        discounted_price.append(np.nan)

                    original = product.find('span', {'class': 'product-strike'})
                    if original is not None:
                        original_price.append(original.text.strip())
                    else:
                        original_price.append(np.nan)

                    discount = product.find('span', {'class': 'product-discountPercentage'})
                    if discount is not None:
                        discount_percentage.append(discount.text.strip())
                    else:
                        discount_percentage.append(np.nan)

                    img = product.find('img', {'class': 'img-responsive'})
                    if img is not None:
                        image.append(img['src'])
                    else:
                        image.append(np.nan)

                    link = product.find('a')
                    if link is not None:
                        partial_reference.append(link['href'])
                    else:
                        partial_reference.append(np.nan)

                    # Extract the rating information
                    rating_container = product.find('div', {'class': 'product-ratingsContainer'})
                    if rating_container is not None:
                        rating_value = rating_container.find('span').text.strip()
                        rating.append(rating_value)
                    else:
                        rating.append(np.nan)

                # Close the webdriver
                driver.quit()

            # Create a pandas dataframe to store the extracted information
                data = {'Brand': brand,
                        'Discount Price': discounted_price,
                        'Original Price': original_price,
                        'Discount Percentage': discount_percentage,
                        #'Image': image,
                        'Partial_url': partial_reference,
                        'Rating': rating}

                df = pd.DataFrame(data)

                parsed_url = urlparse(url)
                base_url = parsed_url.scheme + '://' + parsed_url.netloc + str('/')
                df["complete url"] = base_url + df["Partial_url"]
    #             display(base_url)

                # Drop any rows with missing values
                #df = df.dropna()

                # Reset the dataframe index
                x = df.reset_index(drop=True)

                return x
    def scrape_product_details(self, x):
                """
                Scrapes product details from the URLs in the 'Complete Reference' column of the input dataframe df.

                Args:
                - df: pandas dataframe containing a column named 'Complete Reference' with the URLs of the products

                Returns:
                - pandas dataframe with the scraped data

                """
                # Create an empty list to store the resulting data frames
                df_list = []

                # Iterate through the URLs in df['Complete Reference']
                for url in x['complete url']:
                    driver = webdriver.Chrome()
                    driver.get(url)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    title = soup.find('h1', {'class': 'pdp-name'})
                    if title is not None:
                        title = title.text.strip()
                    else:
                        title = np.nan

                    discounted_price = soup.find('span', {'class': 'pdp-price'})
                    if discounted_price is not None:
                        discounted_price = discounted_price.text.strip()
                    else:
                        discounted_price = np.nan

                    original_price = soup.find('span', {'class': 'pdp-mrp'})
                    if original_price is not None:
                        original_price = original_price.text.strip()
                    else:
                        original_price = np.nan

                    discount_percentage = soup.find('span', {'class': 'pdp-discount'})
                    if discount_percentage is not None:
                        discount_percentage = discount_percentage.text.strip()
                    else:
                        discount_percentage = np.nan

                    offers = soup.find('div', {'class': 'pdp-offers-container'})
                    if offers is not None:
                        offers = offers.text.strip()
                    else:
                        offers = np.nan

                    description = soup.find('p', {'class': 'pdp-product-description-content'})
                    if description is not None:
                        description = description.text.strip()
                    else:
                        description = np.nan

                    size_fitting = soup.find('p', {'class': 'pdp-sizeFitDescContent pdp-product-description-content'})
                    if size_fitting is not None:
                        size_fitting = size_fitting.text.strip()
                    else:
                        size_fitting = np.nan

                    specifications = soup.find('div', {'class': 'index-tableContainer'})
                    if specifications is not None:
                        specifications = specifications.text.strip()
                    else:
                        specifications = np.nan

                    dealer = soup.find('span', {'class': 'supplier-productSellerName'})
                    if dealer is not None:
                        dealer = dealer.text.strip()
                    else:
                        dealer = np.nan

                    related_products = soup.find('ul', {'class': 'product-list-list'})
                    if related_products is not None:
                        related_products = related_products.text.strip()
                    else:
                        related_products = np.nan

                    # images
                    img_list = []
                    images = soup.findAll('div', {'class': 'image-grid-image'})
                    for tag in images:
                        img_list.append(tag['style'].replace('background-image: url(','').replace(');',''))
                    img_list_str = ', '.join(img_list)

                    driver.close()

                    # Create a dictionary with the collected data
                            # Create a dictionary with the collected data
                    data = {'Title': title,
                            'Discounted Price': discounted_price,
                            'Original Price': original_price,
                            'Discount Percentage': discount_percentage,
                            'Offers': offers,
                            'Description': description,
                            'Size & Fitting': size_fitting,
                            'Specifications': specifications,
                            'Dealer': dealer,
                            'Related Products': related_products,
                            'Images': img_list_str,
                            'complete url': url}

                    # Convert data to a dataframe and append it to df_list
                    df_list.append(pd.DataFrame(data, index=[0]))

                # Concatenate all dataframes in df_list and return the resulting dataframe
                    y=pd.concat(df_list, ignore_index=True)

                return y
            
            
    def merge_data(self, df1, df2):
            merged_df = pd.merge(df1, df2, on=['complete url'])
            return merged_df
    
    def extract(self, url):
        x=self.scrape_main_page(url)
        y = self.scrape_product_details(x)
        df = self.merge_data(x, y)
        z = df.drop(['Original Price_y', 'Discount Percentage_y', 'Discounted Price'], axis=1)
        z = df.rename(columns={'Discount Price': 'price', 'Original Price_x': 'mrp', 'Discount Percentage_x': 'discount percentage'})

        return z

if __name__ == '__main__':
    obj = Myntra()
    dataframe = obj.extract('https://www.myntra.com/hoodie?rawQuery=hoodie')
    print(dataframe)
