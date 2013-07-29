#-*- coding: UTF-8 -*-  
import sys
import urllib
import urllib2
import gzip
import StringIO
import re
import json
import base64
import string
import random

import web
import os
import sae
import sae.const
from sae.mail import send_mail 
reload(sys)
sys.setdefaultencoding('utf-8')

from weibopy import OAuthHandler, oauth, API
consumer_key = '159474304'
consumer_secret = '4f846c206e566024b8f11d06faaa24f9'
consumer_url = 'http://apps.weibo.com/ifsissun'
username = '******'
password = '***' 
base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
authheader =  "Basic %s" % base64string

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root+'/../', 'views')
render = web.template.render(templates_root)
db = web.database(dbn='mysql', host=sae.const.MYSQL_HOST,port=int(sae.const.MYSQL_PORT),user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB)
# 页面编码
page_encode = "utf8"

class index:
    def GET(self):
        return render.toolView()



def read(url):
    request = urllib2.Request(url)
    request.add_header("Accept-encoding", "gzip")
    usock = urllib2.urlopen(request)
    page = usock.read()
    # 处理gzip过的页面
    if usock.headers.get('content-encoding', None) == 'gzip':
        page = gzip.GzipFile(fileobj=StringIO.StringIO(page)).read()
     
    # 转unicode(gbk/utf8)
    if not isinstance(page, unicode):
        page = unicode(page, page_encode)
    return page

class ustblib:
    def GET(self):
        # 页面url ison or uid
        ison = web.input().ison
        uid = web.input().uid
        searchUrl = "http://lib.ustb.edu.cn:8080/opac/openlink.php?historyCount=1&strText="+ison+"&doctype=ALL&strSearchType=isbn&match_flag=forward&displaypg=20&sort=CATA_DATE&orderby=desc&showmode=list&location=ALL"
    	page = read(searchUrl)
       
        regUrl=re.findall('item\.php.*?\"',page.replace('\n',''),re.I)
        if regUrl:
            bookUrl = regUrl[0].split('"')[0]
        else : 
            #if not ison then search uid
            searchUid = "http://lib.ustb.edu.cn:8080/opac/openlink.php?historyCount=1&strText="+uid+"&doctype=ALL&strSearchType=isbn&match_flag=forward&displaypg=20&sort=CATA_DATE&orderby=desc&showmode=list&location=ALL"
            pageInUid = read(searchUid)
            regUrlInUid=re.findall('item\.php.*?\"',pageInUid.replace('\n',''),re.I)
            if regUrlInUid:
                bookUrl = regUrlInUid[0].split('"')[0]
            else : 
                #no ison and no uid
                web.header('Content-Type','text/html; charset=UTF-8')
                resHTML = '图书馆还木有，去<a target="_blank" href="http://lib.ustb.edu.cn:8080/asord/asord_redr.php">推荐一下</a>吧'
                return resHTML

        if bookUrl :
            bookPage = read('http://lib.ustb.edu.cn:8080/opac/'+bookUrl)
            info = re.findall('<table.*?<\/table>',bookPage.replace('\n',''),re.I)
            web.header('Content-Type','text/html; charset=UTF-8')
            resHTML = info[0]+'<a target="_blank" href="http://lib.ustb.edu.cn:8080/opac/'+bookUrl+'">check</a>'
            return resHTML.encode("utf-8")


def get_token() : 
    #my weibo account
    os.environ['REMOTE_ADDR'] = '103.8.222.56'
    #get code
    auth = OAuthHandler(consumer_key,consumer_secret,consumer_url)
    params = urllib.urlencode({'action':'submit','withOfficalFlag':'0','ticket':'','isLoginSina':'', \
    'response_type':'code', \
    'regCallback':'', \
    'redirect_uri':consumer_url, \
    'client_id':consumer_key, \
    'state':'', \
    'from':'', \
    'userId':username, \
    'passwd':password, \
    })
    authPage = urllib2.urlopen(auth.get_authorization_url())
    login_url = 'https://api.weibo.com/oauth2/authorize'
    request = urllib2.Request(login_url, params)
    request.add_header("Referer", auth.get_authorization_url())
    codePage = urllib2.urlopen(request)
    code = codePage.geturl().split('code%3D')[1]
    #use code exchange token
    tokenData = 'client_id='+consumer_key+'&client_secret='+consumer_secret+'&grant_type=authorization_code&redirect_uri='+consumer_url+'&code='+code
    request = urllib2.Request("https://api.weibo.com/oauth2/access_token", tokenData)
    tokenPage = urllib2.urlopen(request)
    tokenJson = json.loads(tokenPage.read())
    token = tokenJson['access_token']
   
    db.update('token',where="id =$id", vars={'id':'weibo'}, token = token)

class getToken:
    def GET(self):
        get_token()
        return 1

class if13sis:
    def GET(self):
        token = db.query("SELECT token from token")[0]['token']
        celebrityList = db.select('celebrity')
        for one in celebrityList:
            #get newest mid 
            #weibo开放平台太CD了，不让获取其他用户微博了，只能获取自己的！结果都是空了！
            getFeedUrl= "http://api.weibo.com/2/statuses/user_timeline.json?access_token="+token+"&source="+consumer_key+"&uid="+one['uid']+"&count=1"   
            request = urllib2.Request(getFeedUrl)
            request.add_header("Authorization", authheader)
            handle = urllib2.urlopen(request)
            firstFeed = json.loads(handle.read())
            feed = firstFeed['statuses']
            if feed :
                mid = feed[0]['mid']
            else :
                mid = '0'
            #campare mid
            hasOne = string.atoi(mid) > string.atoi(one['mid'])
            if hasOne :
                db.update('celebrity',where="uid =$uid", vars={'uid':one['uid']}, mid = mid)
                
                #sent e-mail
                msg =  feed[0]['user']['name']+': '+feed[0]['text'].decode('UTF-8')
                send_mail("*****@qq.com", msg,msg,
                  ("smtp.qq.com", 25, "****", "*****", False))

                #favorites feed
                favoritesQuery = urllib.urlencode({"id":mid,"access_token":token,"source":consumer_key})
                favoritesUrl = "http://api.weibo.com/2/favorites/create.json"
                favoritesReq = urllib2.Request(favoritesUrl, favoritesQuery)
                favoritesReq.add_header("Authorization", authheader)
                urllib2.urlopen(favoritesReq)

                #post comment 1937439635:13sis uid
                if one['uid'] == '1937439635' or one['uid'] == '1352528560':
                    if one['uid'] == '1352528560' :
                        comment = "啦啦啦~"
                    else :
                        comment = "13sis重现江湖~"
                    commentQuery = urllib.urlencode({"comment":comment,"id":mid,"access_token":token,"source":consumer_key})
                    commentUrl = "http://api.weibo.com/2/comments/create.json"
                    sendCmtReq = urllib2.Request(commentUrl, commentQuery)
                    sendCmtReq.add_header("Authorization", authheader)
                    urllib2.urlopen(sendCmtReq)

                    #send text message
                    textQuery = urllib.urlencode({"mobile":"1521056****","msg":msg,"encoding":"GB2312"})
                    textUrl = "http://inno.smsinter.sina.com.cn/sae_sms_service/sendsms.php"
                    sendText = urllib2.Request(textUrl, textQuery)
                    hand = urllib2.urlopen(sendText)
                    return hand
        return 1
