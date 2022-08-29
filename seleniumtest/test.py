
#IMPORT STATEMENTS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import csv

# EXCEL DOC
filename = 'testing2123.csv'
# try:
#     os.remove(filename)
# except:
#     print("NO FILE")
f = open(filename, 'a', encoding="utf-8")
f.write("Title" + ',' + "DOI" + ',' + "Publication Date" + ',' + "Issue Date" + ',' + "Volume" + ',' +
        "Issue Number" + ',' + "Start Page" + ',' + "End Page" + ',' + "Abstract" + ',' + "Authors" + ',' +
        "Keywords" + ',' + "Altmetric Score" + ',' + "\n")

# OPEN DRIVER
driver = webdriver.Firefox()
driver.get('https://journals.sagepub.com/toc/mrja/9/4')

# CLEAR COOKIES
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[3]"))
    )
    element.click()
except NameError:
    print("ELEMENT NOT FOUND")

# ISSUE CRAWLER
def crawlPage():
    # GET ISSUE LENGTH
    articles = driver.find_elements(By.CLASS_NAME, 'hlFld-Title')

    # BEGIN CRAWL
    for i in range(len(articles)):
        # ENTER ARTICLE
        articles = driver.find_elements(By.CLASS_NAME, 'hlFld-Title')
        articles[i].click()

        # SCRAPE TITLE
        try:
            title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "publicationContentTitle"))
            )
            title = '"' + title.text + '"'
            print(title)
            f.write(title + ',')
        except:
            print("TITLE ERROR")
            f.write(',')

        # SCRAPE DOI
        try:
            doi = driver.find_element(By.CLASS_NAME, 'doiWidgetLink')
            f.write(doi.text + ',')
        except:
            print("DOI ERROR")
            f.write(',')

        # SCRAPE PUBDATE
        try:
            publication_date = driver.find_element(By.CLASS_NAME, 'publicationContentEpubDate.dates')
            pubdate = '"' + publication_date.text.replace("First Published ", "") + '"'
            f.write(pubdate + ',')
        except:
            print("PUBDATE ERROR")
            f.write(',')

        # OPEN ARTICLE INFO
        try:
            articleinfo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "articleInfoLink"))
            )
            articleinfo.click()
        except:
            print("ARTICLE INFO ERROR")

        # SCRAPE ISSUE DATE
        try:
            issue_date = driver.find_element(By.CLASS_NAME, 'published-dates')
            issue_date = '"' + issue_date.text.split('Issue published: ')[1] + '"'
            f.write(issue_date + ',')
        except:
            print("ISSUE DATE ERROR")
            f.write(',')

        # SCRAPE VOLUME, ISSUE, PAGE
        try:
            volume = driver.find_element(By.CLASS_NAME, 'Article.information div')
            volume = volume.text
            volume_num = volume[8:10]
            issue_num = volume.split(',')[0][-1]
            page_num = volume.split(',')[1].replace(" page(s): ", '')
            page_start = page_num.split('-')[0]
            page_end = page_num.split('-')[1]
            f.write(volume_num + ',' + issue_num + ',' + page_start + ',' + page_end + ',')
        except:
            print("VOLUME ERROR")
            f.write(',,,,')

        # SCRAPE ABSTRACT
        try:
            abstract = driver.find_element(By.CLASS_NAME, 'abstractSection.abstractInFull')
            abstract_text = '"' + abstract.text + '"'
            f.write(abstract_text + ',')
        except:
            print("ABSTRACT ERROR")
            f.write(',')

        # SCRAPE AUTHORS
        try:
            author = driver.find_element(By.CLASS_NAME, 'hlFld-ContribAuthor')
            author_text = '"' + author.text.replace('\n', '') + '"'
            f.write(author_text + ',')
        except:
            print("AUTHOR ERROR")
            f.write(',')

        # SCRAPE KEYWORDS
        try:
            keyword = driver.find_element(By.CLASS_NAME, 'hlFld-KeywordText div')
            keyword = '"' + keyword.text.replace("\n", '') + '"'
            f.write(keyword + ',')
        except:
            print("KEYWORD ERROR")
            f.write(',')

        # SCRAPE ALTMETRIC
        try:
            altmetric = driver.find_element(By.CLASS_NAME, 'section.altmetric-container span a img').get_attribute(
                'alt')
            altmetric_score = altmetric.replace('Article has an altmetric score of ', '')
            f.write(altmetric_score + ',')
        except:
            #print("ALTMETRIC ZERO")
            f.write('0' + ',')

        f.write('\n')
        driver.back()

while True:
    crawlPage()
    try:
        nextPage = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "prev.placedLeft"))
        )
        nextPage.click()
    except:
        break

f.close()
driver.close()
