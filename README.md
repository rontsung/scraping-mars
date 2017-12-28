

```python
# dependencies
# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import json
```


```python
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless = True)
```


```python
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
soup = BeautifulSoup(browser.html, 'html.parser')
title = soup.find('div', 'content_title').text
title

```




    'Mars Mission Sheds Light on Habitability of Distant Planets'




```python
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
soup = BeautifulSoup(browser.html, 'html.parser')
para = soup.find('div', 'article_teaser_body').text
para
```




    'How long might a rocky, Mars-like planet be habitable if it were orbiting a red dwarf star?'




```python
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
soup = BeautifulSoup(browser.html, 'html.parser')
img_url = soup.find('article')['style']
img_url = img_url[img_url.find('(')+2:img_url.find(')')-1]
featured_image_url = 'https://www.jpl.nasa.gov'+img_url
featured_image_url
```




    'https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA19063-1920x1200.jpg'




```python
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)
soup = BeautifulSoup(browser.html, 'html.parser')
t = soup.find_all('p')
for e in t:
    if "Sol" in e.text:
        mars_weather = e.text
        break
mars_weather
```




    'Sol 1910 (Dec 20, 2017), Sunny, high -23C/-9F, low -80C/-112F, pressure at 7.94 hPa, daylight 05:49-17:32'




```python
url = 'http://space-facts.com/mars/'
browser.visit(url)
soup = BeautifulSoup(browser.html, 'html.parser')
t = soup.find('table').find_all('td')
k=0
ok = 0
df = pd.DataFrame({})
df["Property"] = ""
df["Value"] = ""
for e in t:
    if ok % 2 == 0:
        df.at[k, "Property"] = e.text.strip()
        ok += 1
    else:
        df.at[k, "Value"]= e.text.strip()
        ok = 0
        k += 1
df.to_html("df.html", header = False, index = False)
```


```python
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless = True)
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
soup = BeautifulSoup(browser.html, 'html.parser')
ar = soup.find_all('div', 'description')
hemis = []
hemisphere_image_urls = []
for e in ar:
    hemis.append(e.find("h3").text)
for title in hemis:
    new = {}
    browser.click_link_by_partial_href(title[1:title.find(" ")])
    soup = BeautifulSoup(browser.html, 'html.parser')
    img_url = soup.find('div', 'downloads').find('a')['href']
    new["title"] = title
    new["img_url"] = img_url
    hemisphere_image_urls.append(new)
    browser.back()
hemisphere_image_urls
```




    [{'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
      'title': 'Cerberus Hemisphere Enhanced'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
      'title': 'Schiaparelli Hemisphere Enhanced'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
      'title': 'Syrtis Major Hemisphere Enhanced'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg',
      'title': 'Valles Marineris Hemisphere Enhanced'}]


