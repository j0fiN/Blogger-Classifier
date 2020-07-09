# Blog-Classifier

A simple Blog classifier which gives percentage content of C++, Java and Python of a blog.

### To get started
```commandline
git clone 
cd Blog-Classifier
pip install -r requirements.txt
flask run
```

### Instructions to use the api
```python
import requests
response = requests.post(url = '<The local host url>',json = {'blogs':['blog_1', 'blog_2', '...']})
print(response.status_code)
print(response.json())
```
