from bs4 import BeautifulSoup
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

def url_finder():
    res = requests.request("GET",url = 'https://www.fullstackpython.com/blog.html')
    soup = BeautifulSoup(res.content, 'html5lib')
    links = soup.find_all('div', attrs={'class':'c12'})[1]
    links = links.find_all('div', attrs = {'class':'row'})
    url_list = list()
    for i in links:
        url_list.append('https://www.fullstackpython.com'+i.find('a')['href'])
    return url_list


def scrape_blog(link):
    res = requests.request("GET", url=link)
    soup = BeautifulSoup(res.content, 'html5lib')
    if soup.find('div',attrs={'class':'c9'}) is None: return None
    else : blog = [str(i.text) for i in soup.find('div',attrs={'class':'c9'}).find_all(['p','pre'])]
    return "".join(blog)


# def list_blog(url_list):
#     blogs = list()
#     for i in url_list:
#         if scrape_blog(i) is None:continue
#         blogs.append(scrape_blog(i))
#     return blogs

def save(blogs):
    data = pd.DataFrame()
    data["Blog"] = blogs
    data["Target"] = ["python" for _ in range(len(blogs))]
    data.to_csv('''PythonBlogs(withcode).csv''')

if __name__ =="__main__":
    url_list = url_finder()
    processes = list()
    blogs = list()
    with ThreadPoolExecutor(max_workers=len(url_list))  as exe:
        for url in url_list:
            processes.append(exe.submit(scrape_blog,url))

        for process in processes:
            blogs.append(process.result())

    save(blogs)