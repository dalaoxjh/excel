import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://ssr1.scrape.center/'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}


# 新建3个列表，用于存储景点名字nameList、评分scoreList和简介detailList
nameList = []
scoreList = []
detailList = []

writer = pd.ExcelWriter("电影推荐.xlsx")
def getInfo(info_url):
    res = requests.get(info_url, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, "lxml")
    name=soup.find(class_="m-b-sm").text
    nameList.append(name)
    score=soup.find(class_="score m-t-md m-b-n-sm").string.strip()
    scoreList.append(score)
    detail=soup.find(class_="drama").p.text.strip()
    detailList.append(detail)

response = requests.get(url, headers=headers)
html = response.text
soup = BeautifulSoup(html, "lxml")
content_all = soup.find_all(name="a", class_="name")

for content in content_all:
    detail_url  = content.attrs["href"]
    info_url = "https://ssr1.scrape.center" + detail_url
    getInfo(info_url)

total = {"电影名称": nameList, "电影评分": scoreList, "电影简介": detailList}
info = pd.DataFrame(total)
info.to_excel(excel_writer=writer, sheet_name="电影推荐")

writer._save()
