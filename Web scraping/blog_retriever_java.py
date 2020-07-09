from bs4 import BeautifulSoup
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def url_list():
    urls = list()
    for i in range(1,7):
        soup = BeautifulSoup(open(f'java{i}.html', encoding="utf-8"), "html5lib")
        tabs = soup.find_all('div',attrs = {'class':'gsc-webResult gsc-result'})
        for tab in tabs:
            urls.append(tab.find('a',attrs = {'class':'gs-title'})['href'])
    return urls


def scrape_blog(link):
    result = list()
    res = requests.request("GET",url=link)
    soup = BeautifulSoup(res.content, "html5lib")
    di = soup.find('div',attrs={'id':'content'})
    article = di.find("article")
    article = article.find_all(['p','code'])
    for i in article:
        result.append(i.text)
    return "".join(result)

def save(blogs):
    data = pd.DataFrame()
    data["Blog"] = blogs
    data["Target"] = ["java" for _ in range(len(blogs))]
    data.to_csv('''JavaBlogs(withcode).csv''')




if __name__ == "__main__":
    urls = url_list()
    processes = list()
    blogs = list()
    with ThreadPoolExecutor(max_workers=len(urls)) as exe:
        for link in urls:
            processes.append(exe.submit(scrape_blog,link))
        for process in processes:
            blogs.append(process.result())
    save(blogs)

