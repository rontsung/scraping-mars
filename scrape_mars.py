# dependencies
# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd


def scrape():
    data = {}

    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    executable_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    browser = Browser('GOOGLE_CHROME_BIN', **executable_path, headless = True)

    #title and paragraph of latest news
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    soup1 = BeautifulSoup(browser.html, 'html.parser')
    title = soup1.find('div', 'content_title').text
    para = soup1.find('div', 'article_teaser_body').text
    data["title"] = title
    data["blurb"] = para

    #featured image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    soup2 = BeautifulSoup(browser.html, 'html.parser')
    featured_image_url = soup2.find('article')['style']
    featured_image_url = featured_image_url[featured_image_url.find('(')+2:featured_image_url.find(')')-1]
    featured_image_url = 'https://www.jpl.nasa.gov'+featured_image_url
    data["featured"] = featured_image_url

    #latest weather
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    soup3 = BeautifulSoup(browser.html, 'html.parser')
    tweets = soup3.find_all('p')
    for e in tweets:
        if "Sol" in e.text:
            mars_weather = e.text
            break
    data["weather"] = mars_weather

    #facts
    url5 = 'http://space-facts.com/mars/'
    browser.visit(url5)
    soup5 = BeautifulSoup(browser.html, 'html.parser')
    ttt = soup5.find('table').find_all('td')
    k=0
    ok = 0
    df = pd.DataFrame({})
    df["Property"] = ""
    df["Value"] = ""
    for e in ttt:
        if ok % 2 == 0:
            df.at[k, "Property"] = e.text.strip()
            ok += 1
        else:
            df.at[k, "Value"]= e.text.strip()
            ok = 0
            k += 1
    # print(df)
    # print(pp)
    pp = df.to_html(header = False, index = False)
    pp = pp.replace('\n', '')
    data["facts"] = pp

    #hemisphere pics
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    soup4 = BeautifulSoup(browser.html, 'html.parser')
    ar = soup4.find_all('div', 'description')
    labels = []
    hemis = []
    hemisphere_image_urls = []
    for e in ar:
        u= "https://astrogeology.usgs.gov"+e.find('a')['href']
        if u not in hemis:
            hemis.append(u)
    # for name in hemis:
            new = {}
            new["title"] = e.find("h3").text
            browser.visit(u)
            soup5 = BeautifulSoup(browser.html, 'html.parser')
            img_url = soup5.find('div', 'downloads').find('a')['href']
            new["img_url"] = img_url
            hemisphere_image_urls.append(new)
            browser.back()
    data["hemisphere"] = hemisphere_image_urls
    print(data)
    return data
