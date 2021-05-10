# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import requests
from splinter import Browser
import pandas as pd
from requests import get
import os

mars_data={}

def scrape():


        # Set up Splinter
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)


        # Mars News
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)

        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")

        # finding the title   
        title=soup.find_all("div", class_="content_title")

        title=title[1].text

        mars_data["title"]=title

        # finding the paragraph
        paragraph=soup.find('div', class_="article_teaser_body").get_text()

        mars_data["paragraph"]=paragraph

        # getting the image

        url = "https://spaceimages-mars.com/"
        browser.visit(url)
        # Ask Splinter to Go to Site and Click Button with Class Name full_image
        full_image_button = browser.links.find_by_partial_text('FULL IMAGE')
        full_image_button.click()
        html = browser.html
        soup = bs(html, "html.parser")
        image=soup.find('img', class_='fancybox-image').get('src')
        image_url=url + image
        image_url

        mars_data["featured_image_url"]=image_url

        # Scraping the facts
        mars_earth_df= pd.read_html("https://galaxyfacts-mars.com/")[0]
        mars_earth_df.reset_index(inplace=False)
        mars_earth_df.columns=[ "Properties", "Mars", "Earth"]
        mars_earth_df

        # mars_earth table to html
        mars_earth_html = mars_earth_df.to_html(header=False, index=False)

        mars_data["facts"]=mars_earth_html

        # hemispheres

        # URL of page to be scraped
        url = 'https://marshemispheres.com/'

        # Retrieve page with the requests module
        response = requests.get(url)
        # Create BeautifulSoup object; parse with 'html.parser'
        soup_h = bs(response.text, 'html.parser')

        results = soup_h.find_all("div",class_='item')
        # create a list to store dictionaries for title and image links
        hemisphere_image_urls = []
        for result in results:
        #     create a dictionary
                hemi_dict = {}
                titles = result.find('h3').text
                end_link = result.find("a")["href"]
                image_link = "https://marshemispheres.com/" + end_link
                response = requests.get(image_link)
                soup = bs(response.text, 'html.parser')
                downloads = soup.find("div", class_="downloads")
                image_url = "https://marshemispheres.com/" + downloads.find("a")["href"]
                hemi_dict['title']= titles
                hemi_dict['image_url']= image_url
                hemisphere_image_urls.append(hemi_dict)

        # hemisphere_image_urls

        mars_data["hemisphere"]=hemisphere_image_urls


        # Close the browser after scraping
        browser.quit()

        # Return results
        return mars_data


