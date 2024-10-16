Installiing the Libraries -
 numpy,pandas,requests,BeautifulSoup,selenium    using command ( pip install {library_name} )



For 'selenium webdriver' visit website - "[https://chromedriver.chromium.org/downloads](https://googlechromelabs.github.io/chrome-for-testing/#stable)"
Select 
      Binary - Chrome Driver
      Platform - 'as per ur us device' [windows,linux]
      URL - copy and paste the url in browser to download the driver . 

step 1: Install the latest webdriver which fits with your Chrome browser .

step 2: After installing the driver go to properties and copy path of the driver .


step 3: Changing the Driver path in function - 
                                      class Amazon:
                                              def __init__(self, driver=r'"C:\Users\DELL\Downloads\WEB SCRAPING\chromedriver_win32_new"'):
                                                  self.driver = webdriver.Chrome(driver)
                                                  
change this path to the path you have copied from step 2 -  
                                      class Amazon:
                                              def __init__(self, driver=r'{your_driver_path}'):
                                                  self.driver = webdriver.Chrome(driver)
