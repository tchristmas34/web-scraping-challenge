# Dependencies

from bs4 import BeautifulSoup as bs

from splinter import Browser

import pandas as pd

import os

import time

import requests



def init_browser():

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

    return Browser("chrome", **executable_path, headless=False)



def scrape():

    browser = init_browser()



    # Create Link to NASA

    url_nasa = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    browser.visit(url_nasa)

    html = browser.html



    # Parse HTML

    soup_nasa = bs(html, "html.parser")



    # Extract Article

    article_nasa = soup_nasa.find("div", class_='list_text')

    title_nasa = article_nasa.find("div", class_="content_title").text

    teaser_nasa = article_nasa.find("div", class_ ="article_teaser_body").text



        # Create Link to JPL

    url_JPL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url_JPL)



    # Click On 'Full Image'

    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(5)



    # Click On 'More Info'

    browser.click_link_by_partial_text('more info')



    # Parse HTML

    html = browser.html

    image_JPL = bs(html, 'html.parser')



    # Scrape the URL

    url_JPL_image = image_JPL.find('figure', class_='lede').a['href']

    url_JPL_full_image = f'https://www.jpl.nasa.gov{url_JPL_image}'



    # Create Link to Twitter

    url_twitter = "https://twitter.com/marswxreport?lang=en"

    request_twitter = requests.get(url_twitter)



    # Parse HTML

    soup_twitter = bs(request_twitter.text, 'html.parser')



    # Iterate over Tweets to Obtain All Text

    mars_weather_tweets = [p.text for p in soup_twitter.findAll('p', class_='tweet-text')]



    # Pull Latest Tweet

    mars_weather = mars_weather_tweets[0]



    # Create Link to Space Facts

    url_facts = 'https://space-facts.com/mars/'



    # Find All Tables and Pull Out Mars Information

    fact_table = pd.read_html(url_facts)

    mars_facts_df = fact_table[0]

    mars_facts_df.rename(columns={0:"Descriptions", 1:"Mars"}, inplace=True)

    mars_facts_df = mars_facts_df.set_index("Descriptions")



    # Create HTML Table String

    html_table = mars_facts_df.to_html(classes="table table-striped")



    # Create Link to USGS

    url_USGS = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(url_USGS)

    html = browser.html



    # Parse HTML

    soup_USGS = bs(html, 'html.parser')



    # Create List For Images

    mars_hemisphere = []



    # Retrieve All Picture Code

    results = soup_USGS.find("div", class_ = "result-list" )

    hemispheres = results.find_all("div", class_="item")



    # Iterate Through Each Hemisphere

    for hemisphere in hemispheres:

        title = hemisphere.find("h3").text

        title = title.replace("Enhanced", "")

        end_link = hemisphere.find("a")["href"]

        image_link = "https://astrogeology.usgs.gov/" + end_link    

        browser.visit(image_link)

        html = browser.html

        soup = bs(html, "html.parser")

        downloads = soup.find("div", class_="downloads")

        image_url = downloads.find("a")["href"]

        mars_hemisphere.append({"title": title, "img_url": image_url})



    # Store Data In a Dictionary

    mars_data = {

        "title_nasa": title_nasa,

        "teaser_nasa": teaser_nasa,

        "url_JPL_full_image": url_JPL_full_image,

        "mars_weather": mars_weather,

        "html_table": html_table,

        "mars_hemisphere": mars_hemisphere

    }



    # Close Browser

    browser.quit()



    # Return Results

    return mars_data



if __name__ == '__main__':

    scrape()