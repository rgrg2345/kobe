#encoding utf-8
import requests
from bs4 import BeautifulSoup
import re
import base64
import shutil


API_URL='https://api.imgur.com/'

class Imgur_Client(object):


  def __init__(self,client_id,client_secret):
    self.client_id=client_id
    self.client_secret=client_secret
    self.session=None
    self.img_url=None
    self.acc_token=None
    self.ref_token=None

  def get_client_id(self):
    return self.client_id

  def get_auth_url(self,resp_type='pin'):
    return '%soauth2/authorize?client_id=%s&response_type=%s'%(API_URL,self.client_id,resp_type)

  def prepare_headers(self,anon=False):
    headers={}

    if anon or self.session is None:
      if self.client_id is None:
        raise 'Error'
      else:
        headers['Authorization'] = 'Client-ID %s' % self.get_client_id()
    else:
      headers['Authorization'] = 'Bearer %s' % self.get_current_access_token()

    return headers

  def get_current_access_token(self):
    return self.acc_token

  #always use pin method
  def authorize(self,grant_type='pin'):
    self.pin=self.get_pin()

    print 'Authorizing..'
    payload={
        'client_id':self.client_id,
        'client_secret':self.client_secret,
        'grant_type':grant_type,
        'pin':self.pin
        }
    rs=requests.session()

    headers=self.prepare_headers(True)

    url='%soauth2/token'%API_URL

    res=rs.post(url,headers=headers,data=payload)

    #if status code =403 means error
    #               =200 means success
    if res.status_code==200:
      print 'Authorization success!!'
      res_data=res.json()
      self.acc_token=res_data['access_token']
      self.ref_token=res_data['refresh_token']
      print 'access token: '+self.acc_token,'\nrefresh token: '+self.ref_token
      self.session=rs
    elif res.status_code==403:
      print 'Authorization error'

  def get_pin(self):

    rs=requests.session()

    #First access to get token
    auth_url=self.get_auth_url('pin')
    print 'Get pin ..'
    res=rs.get(auth_url)

    payload={
      'username’:’accoubt’,
      'password’:’password’,
      'allow':rs.cookies.get('authorize_token'),
      '_jafo[activeExperiments]':[],
      '_jafo[experimentData]':{}
    }

    res=rs.post(auth_url,data=payload)
    code =BeautifulSoup(res.text,"html.parser")

    """find pin code in <link ref="canonical"...>"""
    r=code.find('link',rel='canonical')
    m=re.search('pin=.+" rel',str(r))

    pin=''
    if m :
      s=m.group()
      pin=s[4:len(s)-5]
    return pin

  def upload(self,img,types):

    if types == 'img':
      payload={
        'image':img,
        'type': 'base64'
        }
    else:
    #url data
      payload={
        'image':img,
        'type':'url'
      }

    headers=self.prepare_headers(False)
    res=self.session.post('%s3/image'%API_URL,headers=headers,data=payload)

    if res.status_code==200:
      print '\nImage Upload Success!!'
      res_data=res.json()
      self.img_url=res_data[u'data'][u'link']
    elif res.status_code==403:
      self.refresh()
      self.upload(img,types)
    else:
      print  'Error code   %s'%res.status_code

  def refresh(self):
    url=API_URL+'oauth2/token'

    payload={
        'client_id':self.client_id,
        'client_secret':self.client_secret,
        'refresh_token':self.ref_token,
        'grant_type': 'refresh_token'
        }
    res=requests.post(url,data=payload)
    if res.status_code != 200:
      raise 'Refresh Error'

    res_data=res.json()
    self.acc_token=res_data['access_token']

def creat_client():
  client=Imgur_Client(‘client_id’,’client_secret’)

  #authorization flow
  client.authorize()

  return client

def url2imgur(client,url):

  client.upload(url,'url')

  return client.img_url


def img2imgur(client,img):

  client.upload(base64.b64encode(img),'img')

  return client.img_url

def url2img(url):
  res=requests.get(url,stream=True)
  img=res.raw.read(decode_content=True)
  del res
  return img


if __name__=='__main__':

  """three ways to upload image"""
  client=creat_client()
  #upload image from url directly
  print url2imgur(client,'http://i.imgur.com/Z2z4YiF.png'),'\n\n'


  #read image from file and upload
  with open('imgur.png','rb') as f:
    print img2imgur(client,base64.b64encode(f.read()))

  #read file-like image  from url and upload
  img=url2img('http://i.imgur.com/Z2z4YiF.png')
  b64=base64.b64encode(img)
  print img2imgur(client,b64)


