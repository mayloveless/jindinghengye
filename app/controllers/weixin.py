#-*- coding: UTF-8 -*- 
import web
import os
import sae
import sae.const
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root+'/../', 'views')
render = web.template.render(templates_root,base='layout')
db = web.database(dbn='mysql', host=sae.const.MYSQL_HOST,port=int(sae.const.MYSQL_PORT),user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB)


TOKEN = 'jdhy'
class index:
    def GET(self):
        
        echoStr = web.input().get('echostr')
        signature = web.input().get('signature')
        timestamp = web.input().get('timestamp')
        nonce = web.input().get('nonce')
        arr = [TOKEN,timestamp,nonce]
        tmpArr = sorted(arr)
        tmpStr = ''.join(tmpArr)
        tmpStr = hashlib.sha1(tmpStr.encode("utf8")).hexdigest()
        if tmpStr == signature :
            return echoStr
        else :
            return 0
    
     def POST(self):
        x = web.input()
        #严重没有调，完全不可信
        if x !=='' :

            plistQuery = "SELECT * from product inner join cata on product.cata=cata.cataId WHERE 1 = instr(product,$key) or  1 = instr(cataName,$key) or  1 = instr(backup,$key) or  1 = instr(factory,$key) or  1 = instr(size,$key) order by productId ASC limit $offset,$pageNum"
            productList = db.query(plistQuery,vars={'key':web.input()['HTTP_RAW_POST_DATA']})
            
            if not productList :
                str = ' <xml>'+
                         '<ToUserName>11</ToUserName>'+
                         '<FromUserName>11</FromUserName> '+
                         '<CreateTime>1</CreateTime>'+
                         '<MsgType>text</MsgType>'+
                         '<Content>find but not find</Content>'+
                         '<MsgId>1234567890123456</MsgId>'+
                        '</xml>'
                return str
            else :
                str = ' <xml>'+
                         '<ToUserName>11</ToUserName>'+
                         '<FromUserName>11</FromUserName> '+
                         '<CreateTime>1</CreateTime>'+
                         '<MsgType>text</MsgType>'+
                         '<Content>find && find</Content>'+
                         '<MsgId>1234567890123456</MsgId>'+
                        '</xml>'
                return str
        
        else :
            str = 'Input something...'
            return str


       

            

