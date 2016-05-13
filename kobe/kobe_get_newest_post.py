#encoding utf-8
import requests
from bs4 import BeautifulSoup
import kobe_get_post_image
import kobe_get_post
import copy2file
import oauth2

DOWNLOAD_POST_QUANTITY = 30

def get_newest_url():
  url='https://engineer.kobe.ga/latest'

  res=requests.get(url)
  code=BeautifulSoup(res.text,"html.parser")

  hashtag=int(code.select('title')[0].text[14:])
  print 'latest hashtag : %d'%hashtag

  #initialize
  uploadlist=[]
  client=None

  for i in range(DOWNLOAD_POST_QUANTITY):
    #image url
    url=kobe_get_post_image.url2imgurl(kobe_get_post.hashtag2url(hashtag-i))

    #skip invalid url
    if url == None:
      continue

    #using same client to upload image
    if client==None:
      client=oauth2.creat_client()
    uurl=oauth2.url2imgur(client,url)
    uploadlist.append('hashtag : %d   %s\n'%(hashtag-i,uurl))

  copy2file.copy('upload',copy2file.list2str(uploadlist),1)

if __name__=='__main__':
  get_newest_url()
