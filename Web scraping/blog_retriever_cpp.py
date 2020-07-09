from bs4 import BeautifulSoup
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

def url_list():
    # response = requests.request("GET", url="https://www.bfilipek.com/")
    # print(response.status_code)
    html = BeautifulSoup(open('cpp.html', encoding="utf8"), "html5lib")
    division = html.find('div',attrs={'class':'blog-posts hfeed'})
    division = division.find_all('div',attrs={'class':'date-outer'})
    urls = list()
    for blog in division:
        link = blog.find('h2',attrs={'class':'post-title entry-title'})
        link = link.find('a')['href']
        urls.append(link)
    return urls

def scrape_blog(link):
    res = requests.request("GET", url = link)
    soup = BeautifulSoup(res.content, "html5lib")
    container = soup.find('div',attrs={'class':'post hentry'})
    blog = [str(i.text) for i in container.find_all(['p','pre'])]
    return ''.join(blog)

def save(blogs):
    data = pd.DataFrame()
    data["Blogs"] = blogs
    lang = ["cpp" for _ in blogs]
    data["Target"] = lang
    data.to_csv("""CppBlogs(with code).csv""")





if __name__ =="__main__":
    urls = url_list()
    blogs = list()
    processes = list()
    s = time.time()
    with ThreadPoolExecutor(max_workers=len(urls)) as exe:
        for link in urls:
            processes.append(exe.submit(scrape_blog, link))
        for process in processes:
            blogs.append(process.result())
    f = time.time()
    print(len(blogs)," ",f-s," sec")
    save(blogs)

    # bloger = list()
    # s = time.time()
    # for i,c in enumerate(url_list()):
    #     bloger.append(scrape_blog(c))
    # f = time.time()
    # print(f-s," sec")