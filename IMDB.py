import pandas as pd
import requests
from bs4 import BeautifulSoup 
import numpy as np
from urllib.parse import urlparse
from selenium import webdriver
import time
import numpy as np
import pandas as pd 
from bs4 import BeautifulSoup
import re

class Imdb:
    def __init__(self):
        pass

    def scrape_main_page(self, url):
        movie_name = []
        year = []
        time = []
        rating = []
        metascores = []
        votes = []
        gross = []
        partial_links = []
        
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

        for store in movie_data:
            partial = store.h3.a['href']
            
            partial_links.append(partial)
            
            name = store.h3.a.text if store.h3.a is not None else np.nan
            movie_name.append(name)

            year_of_release = store.h3.find('span', class_='lister-item-year text-muted unbold')
            if year_of_release is not None:
                year_of_release = year_of_release.text.replace('(', '').replace(')', '')
            else:
                year_of_release = np.nan
            year.append(year_of_release)

            runtime = store.p.find('span', class_='runtime')
            if runtime is not None:
                runtime = runtime.text.replace('min', '')
            else:
                runtime = np.nan
            time.append(runtime)

            rate = store.find('div', class_='inline-block ratings-imdb-rating')
            if rate is not None:
                rate = rate.text.replace('\n', '')
            else:
                rate = np.nan
            rating.append(rate)

            value = store.find_all('span', attrs={'name': 'nv'})

            vote = value[0].text if value else np.nan
            votes.append(vote)

            grosses = value[1].text if len(value) > 1 else np.nan
            gross.append(grosses)

            metascore = store.find('span', class_='metascore')
            if metascore is not None:
                metascore = metascore.text.strip()
            else:
                metascore = np.nan
            metascores.append(metascore)

        movie_df = pd.DataFrame({  'Name of movie': movie_name, 'Year of release': year, 'Watchtime (mins)': time, 'Movie Rating': rating, 'Metascore': metascores, 'Votes': votes, 'Gross Collection': gross ,'Partial_url': partial_links})
        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + '://' + parsed_url.netloc
        movie_df["complete url"] = base_url + movie_df["Partial_url"]
        x = movie_df.dropna()
        x.reset_index(inplace=True)

        #printing the result
        return x
    
    def scrape_movie_data(self,x):
        # Create a webdriver
        driver = webdriver.Chrome("C:/Users/User/chromedriver.exe")

        # Create the DataFrame
        # Create an empty list to store rows
        rows_list = []

        # Loop through the URLs in the "Complete Link" column of the input DataFrame
        for url in x['complete url']:
            # Open the website
            driver.get(url)

            # Extract the html page
            html = driver.page_source
           # soup = BeautifulSoup(html, 'html.parser')
            # response = requests.get(url)
            soup = BeautifulSoup(html, 'html.parser')

            # Extract the movie title
            title = soup.find("div", attrs={"class": "sc-b5e8e7ce-1 kNhUtn"})
            if (title != None):
                movie_title = title.h1.text
            else:
                movie_title = np.nan

            poster = soup.find("a", attrs={"class":"ipc-lockup-overlay ipc-focusable"})
            if (poster!=None):
                poster=poster.get("href")
                poster = "https://www.imdb.com/" + poster
            else:
                poster = np.nan

            trailer = soup.find("video", attrs={"class":"jw-video jw-reset"})
            if (trailer!=None):
                trailer=trailer.get("src")
            else:
                trailer = np.nan

            tags = soup.find("div", attrs={"class":"ipc-chip-list__scroller"})
            if (tags!=None):
                tags=tags.text
            else:
                tags = np.nan

            storyline = soup.find("div", attrs={"class":"ipc-html-content-inner-div"})
            if (storyline!=None):
                extra = soup.find("a", attrs={"class":"ipc-link ipc-link--base sc-434f87dd-0 livonz"})
                if (extra!=None):
                    extra=extra.text
                    storyline=storyline.text.replace(extra,'')
                else:
                    storyline = storyline.text
            else:
                storyline = np.nan

            cast = soup.find("div", attrs={"class":"ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid"})
            if (cast!=None):
                cast=cast.text
            else:
                cast = np.nan

            simi = soup.find_all("div", attrs={"class":"ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--nowrap ipc-shoveler__grid"})
            if (simi!=None and len(simi)>=3):
                similar = simi[2]
                if (similar!=None):
                    similar=similar.text.replace('Watch options','').replace('Watchlist','').replace('1','  ').replace('2','  ').replace('3','  ').replace('4','  ').replace('5','  ').replace('6','  ').replace('7','  ').replace('8','  ').replace('9','  ').replace('10','  ').replace('.','  ').replace(':','  ')
            else:
                similar = np.nan

            # Append the values as a dictionary to the rows_list
            rows_list.append({
                'Poster': poster,
                'Trailer': trailer,
                'Tags': tags,
                'Storyline': storyline,
                'Cast': cast,
                'Similar Movies':similar,
                'complete url':url})

        # Create a new DataFrame using the rows_list
        y = pd.DataFrame(rows_list)

        # driver.quit()

        return y

    def merge_data(self, df1, df2):
        merged_df = pd.merge(df1, df2, on=['complete url'])
        return merged_df
    
    def extract(self, url):
        x=self.scrape_main_page(url)
        y = self.scrape_movie_data(x)
        z = self.merge_data(x, y)
        return z

if __name__ == '__main__':
    # Call the generate_report() function on the DataFrame
    obj =Imdb()
    z = obj.extract('https://www.imdb.com/search/title/?title_type=feature&year=2000-01-01,2000-12-31&start=101')
    print(z)
  