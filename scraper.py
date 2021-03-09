import requests
import re
from dateutil import parser
import json
from datetime import date, datetime
from bs4 import BeautifulSoup

# Get current date
today = date.today()

# Get list of companies
currentline = []
with open("company_list.txt", "r") as filestream:
    for line in filestream:
        currentline = line.split(",")


def findnth(haystack, needle, n):
    parts = haystack.split(needle, n+1)
    if len(parts) <= n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)


# File to write results
f = open("results.txt", "w")
f.write("Pharma Companies News and Releases for Today\n")

for url in currentline:
    print('Processing URL:', url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Make the BS requests first to get the data
    if url == "https://investor.onconova.com/press-releases":
        curr_date_datetime = str(soup.find_all(
            "time", {"class": "datetime"})[0].string)
        curr_date_results = soup.find_all(
            "td", {"headers": "view-field-nir-news-title-table-column"})
        curr_date_headline = ""
        index = 0
        for tag in curr_date_results:
            if index > 0:
                break
            aTags = tag.find_all("a")[0].string
            res = re.split(', |>|<|!', aTags)
            index += 1
            curr_date_headline = res[0].split("\n")[0].strip()
    elif url == "https://ir.ocugen.com/news-releases":
        curr_date_datetime = str(soup.find_all(
            "div", {"class": "nir-widget--field nir-widget--news--date-time"})[0].string)
        curr_date_results = soup.find_all(
            "article", {"role": "article"})
        curr_date_headline = ""
        index = 0
        for tag in curr_date_results:
            if index > 0:
                break
            aTags = tag.find_all("a")[0].string
            res = re.split(', |>|<|!', aTags)
            index += 1
            curr_date_headline = res[0].split("\n")[0].strip()
    elif url == "https://ir.kintara.com/press-releases":
        curr_date_datetime = str(soup.find_all(
            "div", {"class": "date"})[0].string)
        curr_date_results = soup.find_all(
            "h2", {"class": "media-heading"})
        curr_date_headline = ""
        index = 0
        for tag in curr_date_results:
            if index > 0:
                break
            aTags = tag.find_all("a")[0].string
            res = re.split(', |>|<|!', aTags)
            index += 1
            curr_date_headline = res[0].split("\n")[1].strip()
    else:
        curr_date_datetime = str(soup.find_all(
            "div", {"class": "nir-widget--field nir-widget--news--date-time"})[0].string)
        curr_date_headline = str(soup.find_all(
            "div", {"class": "nir-widget--field nir-widget--news--headline"})[0].string)

    # If the article's date matches today, enter logic to add results to solution
    if parser.parse(curr_date_datetime.strip()).date() == datetime.today().date():
        # If we find an article relating to today, add to the dictionary
        if curr_date_headline != 'None':
            f.write("On " + curr_date_datetime.strip() + " " +
                    url + " posted : " + curr_date_headline + "\n")
        else:
            curr_date_headline = str(soup.find_all(
                "div", {"class": "nir-widget--field nir-widget--news--headline"})[0].contents)
            res = re.split(', |>|<|!', curr_date_headline)
            f.write("On " + curr_date_datetime.strip() + " " +
                    url + " posted : " + res[3].strip() + "\n")

f.close()
