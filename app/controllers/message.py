#-*- coding: UTF-8 -*- 
import web
import os
import sae
import sae.const
from sae.mail import send_mail 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root+'/../', 'views')
render = web.template.render(templates_root,base='layout')

db = web.database(dbn='mysql', host=sae.const.MYSQL_HOST,port=int(sae.const.MYSQL_PORT),user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB)

class index:
    def GET(self):
    	indexObj = {'isJustDone':0}
        return render.message(indexObj)

            
    def POST(self):
        x = web.input()

        db.insert('message', name = x.name, contact = x.contact,factory = x.factory,content = x.content)
        indexObj = {'isJustDone':1}

        msg =  '姓名：'+x.name+'；联系方式：'+x.contact+';来自：'+x.factory+';内容：'+x.content.decode('UTF-8')
        send_mail(["*****","*****@qq.com"], '【金鼎恒业网站信息】来自：'+x.name+'的留言',msg,
          ("smtp.qq.com", 25, "******@qq.com", "*****", False))
     	
        return render.message(indexObj)
