# spider - main.py
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class QuotesSpider(scrapy.Spider):
    name = "ipl"

    def start_requests(self):
        # Set up ChromeOptions to configure Chrome browser
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # Setting up the Chrome WebDriver with options
        driver = webdriver.Chrome(options=chrome_options)
        
        # Replace '' with the URL you want to scrape
        driver.get('https://books.toscrape.com/')
        
        # Find all link elements with the CSS selector 'div.image_container>a'
        link_elements = driver.find_elements(By.CSS_SELECTOR, 'div.image_container>a')
        
        # Iterate through each link element and yield a request for each link
        for link_element in link_elements:
            # Get the 'href' attribute of the link element
            link_href = link_element.get_attribute('href')
            # Yield a Scrapy request for each link with the parse method as the callback
            yield scrapy.Request(link_href, callback=self.parse)
        
        # Closing the browser
        driver.quit()

    def parse(self, response):
        # Process the response and extract the data
        yield {
            # Extract the 'Price' information using XPath
            'price': response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td/text()').get(),
            # Extract the 'UPC' information using XPath
            'upc' : response.xpath('//th[text()="UPC"]/following-sibling::td/text()').get()
        }