from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")
import re
import pandas as pd
import xlrd
from tqdm import tqdm

options = Options()
options.headless = True

input_df = pd.read_excel("ios_appstoreurl.xlsx")

output_df_list = []

for rows_num in tqdm(range(0, input_df.shape[0])):

    app_creator_name = input_df["Company Name"][rows_num]
    app_website_name = input_df["Website"][rows_num]
    url = input_df["Appstore"][rows_num]
    url = str(url)
    url = url.split("?")[0]
    url = url + "?ign-mpt=uo%253D4#see-all/developer-other-apps"
    browser = webdriver.Firefox(executable_path = 'geckodriver',options=options)
    try:
        browser.get(url)
    except:
        print("{} Not found".format(app_creator_name))
        browser.quit()
        continue
    time.sleep(30)
    html_source=browser.page_source

    browser.quit()

    soup = BeautifulSoup(html_source, 'html.parser')

    container = soup.findAll("div", {"class": "l-row"})

    url_list = []
    print(url)

    for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
        url_link = str(link.get('href'))
        if "/app/" in url_link:
            url_list.append(url_link)

    for url_links in url_list:
        print([app_creator_name,url_links])
        output_df_list.append([app_creator_name,app_website_name,url_links])

    output_df = pd.DataFrame(output_df_list ,columns = ["Company Name","Website","AppStore Urls"])
    print(output_df)
    output_df.to_excel("ios_appstoreurl_output.xlsx",index=False)