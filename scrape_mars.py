# import necessary libraries
from flask import Flask, render_template
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def mars_scrape():

    browser = init_browser()
    
    url = 'https://mars.nasa.gov/news'
    response = requests.get(url)
    time.sleep(3)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'lxml')

    news_title = soup.find('div', class_='content_title').text.strip()

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')
    time.sleep(3)

    news_p = soup.find('div', class_='article_teaser_body').text.strip()

    # # JPL Mars Images

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    html = browser.html
    soup = bs(html, 'html.parser')

    base_url = 'https://www.jpl.nasa.gov'
    image_url = soup.find('a', class_='button fancybox')['data-fancybox-href']

    featured_image_url = base_url + image_url

    # # Mars Weather

    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text


    # # Mars Facts

    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)

    df = tables[0]

    html_table = df.to_html(index = False)

    hemisphere_image_urls = []

    # Cerebus hemisphere
    url4 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url4)

    html = browser.html
    soup = bs(html, 'html.parser')

    title_cerebus = soup.find('h2', class_='title').text
    
    img_cerebus = soup.find('a', text='Sample')['href']

    #Valles Marineris
    url5 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url5)

    html = browser.html
    soup = bs(html, 'html.parser')

    title_valles = soup.find('h2', class_='title').text

    img_valles = soup.find('a', text='Sample')['href']
    
    # Schiaparelli
    url6 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url6)

    html = browser.html
    soup = bs(html, 'html.parser')

    title_schiaparelli = soup.find('h2', class_='title').text
    
    img_schiaparelli = soup.find('a', text='Sample')['href']

# Syrtis Major
    url7 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url7)

    html = browser.html
    soup = bs(html, 'html.parser')

    title_syrtis = soup.find('h2', class_='title').text

    img_syrtis = soup.find('a', text='Sample')['href']

    hemisphere_image_urls.append({'title': title_cerebus, "img_url": img_cerebus})
    hemisphere_image_urls.append({'title': title_valles, "img_url": img_valles})
    hemisphere_image_urls.append({'title': title_schiaparelli, "img_url": img_schiaparelli})
    hemisphere_image_urls.append({'title': title_syrtis, "img_url": img_syrtis})

    browser.quit()

    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'html_table': html_table,
        'hemisphere_image_urls': hemisphere_image_urls
        }
    
    return mars_data
