#encoding utf-8
import requests
from bs4 import BeautifulSoup
import shutil
import re

import oauth2
def get_post_image(url):


  rs=requests.session()
  res=rs.get(url)
  code =BeautifulSoup(res.text,"html.parser")

  #print code
  lst=re.findall('(?:"https://scontent).{1,200}&amp;oe=\w{8}',str(code))

  return lst

def url2imgurl(url):
  lst=get_post_image(url)
  if len(lst)==2:
    return reconstruct(lst[1])
  return None
def dl2png(lst,name):

    #when only match one imply not use image post
    #no match imply post were deleted
  if len(lst)==2:
    img_url=reconstruct(lst[1])

    res2=requests.get(img_url,stream=True) #open as stream to read image

    f=open('%d.png'%(name),'wb')
    shutil.copyfileobj(res2.raw,f)
    f.close()
    del res2 #delete buffer

  else:
    pass

def reconstruct(s):
  return s[1:len(s)-15]+s[len(s)-11:]
if __name__=='__main__':
  url='https://www.facebook.com/kobeengineer/posts/1764944913741778'
  #dl2png(url,'test')
  #print oauth2.url2imgur(url2imgurl(url))
