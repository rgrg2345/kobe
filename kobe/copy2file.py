#encoding utf-8
import re
from os.path import exists
import sys

#set encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

def list2str(li):
    string=''
    for item in li:
      string+=item
    return string

def copy(fileName,text,mode):#mode 0: not overwrite
                             #     1: overwrite
                             #     2:append
  if mode!=0:
    if mode==2:
      f=open('%s%s'%(fileName,'.txt'),'ab')
    else:
      f=open("%s%s"%(fileName,'.txt'),"wb")

    f.write(text)
    print 'Copy to %s'%(f.name)
    f.close()

