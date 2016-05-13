#encoding utf-8
import requests
from bs4 import BeautifulSoup
import re

"""hashtag convert to facebook post url"""
def hashtag2url(hashtag):
  url='https://engineer.kobe.ga/hashtag/%d'%hashtag

  res=requests.get(url)
  code=BeautifulSoup(res.text,"html.parser")

  for item in code.select('html'):
    for subitem in item.select('.fb-post'):
      m=re.search('https://.+"',str(subitem))
      if m :
        s=m.group()
        url=s[:len(s)-1]
      break
  return url
if __name__=='__main__':
  print  hashtag2url(2)
