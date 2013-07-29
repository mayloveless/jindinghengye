import web
import os
import sae
import time 
import hashlib
import sae.const
import sae.storage
from StringIO import StringIO
from PIL import Image

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root+'/../', 'views')
render = web.template.render(templates_root)
db = web.database(dbn='mysql', host=sae.const.MYSQL_HOST,port=int(sae.const.MYSQL_PORT),user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB)
saeStorage= sae.storage.Client(prefix='wangaibing')
pageNum  = 30

def checkLogin():
    ssid = hashlib.md5()
    ssid.update('jindinghengye') 
    cookie = web.cookies() 
    if not web.cookies().get('sid') or web.cookies().get('sid') != ssid.hexdigest():
        raise web.seeother('/login')


class index:
    def GET(self):
        checkLogin()

        indexObj = {}
        cataList = db.select('cata')
        indexObj['cata'] = cataList
        indexObj['wrong'] = 0 
        indexObj['curPage'] = web.input().get('page') and int(web.input().get('page'))+1 or 1
        offsetNum= int(indexObj['curPage']-1)*pageNum 

        if web.input().get('cata'):

            plistQuery = "SELECT * from product inner join cata on product.cata=cata.cataId  where product.cata = $id order by productId ASC limit $offset,$pageNum"
            productList = db.query( plistQuery,vars={'id':web.input()['cata'],'pageNum':pageNum,'offset':offsetNum})
            indexObj['pCount'] =  db.query("SELECT count(*) FROM product where cata = $id",vars={'id':web.input()['cata']}).list()[0]['count(*)']
        else :
            plistQuery = "SELECT * from product inner join cata on product.cata=cata.cataId order by productId ASC limit $offset,$pageNum"
            productList = db.query(plistQuery,vars={'pageNum':pageNum,'offset':offsetNum})
           
            indexObj['pCount'] =  db.query("SELECT count(*) FROM product").list()[0]['count(*)']

        indexObj['curCata'] = web.input().get('cata') and web.input().get('cata') or 0
        if not productList :
            indexObj['product'] = {}
            indexObj['pCount'] = 0
            indexObj['pages'] = 0
            return render.admin(indexObj)
        else :
            indexObj['product'] = productList
            indexObj['pages'] = indexObj['pCount'] % pageNum and indexObj['pCount']/pageNum+1 or indexObj['pCount']/pageNum 

            return render.admin(indexObj)

class delete:
    def POST(self):
        pid = web.data().split('=')[1]
        num = db.delete('product', where="productId=$id",vars={'id':pid})
        return 1

class edit:
    def POST(self):
        x = web.input(imgFile={})

        if not x.name or not x.size or not x.factory :
            raise web.seeother('/admin')
       
        if x.imgFile.filename:
            'watermark'
            source_img = Image.open(StringIO(x.imgFile.file.read()))
            logo_img = Image.open('./static/img/waterMark.png')
            source_img.paste(logo_img, ((source_img.size[0] - logo_img.size[0])/2,
                     (source_img.size[1] - logo_img.size[1])/2), logo_img)
            markImg = source_img.tostring('jpeg', 'RGB')

            filename=  str(int(time.time())) +'.'+x.imgFile.filename.replace('\\','/').split('.')[1]
            ob = sae.storage.Object(markImg)
            url = saeStorage.put('wangaibing', filename, ob)
            db.update('product',where="productId =$pid", vars={'pid':x.pid}, product = x.name, size = x.size,factory = x.factory,backup = x.backup,cata = x.cata,pic = url,isMine = x.isMine)
        else :
            db.update('product', where="productId =$pid", vars={'pid':x.pid},product = x.name, size = x.size,factory = x.factory,backup = x.backup,cata = x.cata ,isMine = x.isMine)

        raise web.seeother('/admin')



class add:
    def GET(self):
        checkLogin()

        indexObj = {}
    	cataList = db.select('cata')
        indexObj['cata'] = cataList
        indexObj['wrong'] = 0
        return render.add(indexObj)
    def POST(self):
        x = web.input(imgFile={})
        if not x.name or not x.size or not x.factory or not x.imgFile.filename :
            indexObj = {}
            cataList = db.select('cata')
            indexObj['cata'] = cataList
            indexObj['wrong'] = 1
            return render.add(indexObj)

        'watermark'
        source_img = Image.open(StringIO(x.imgFile.file.read()))
        logo_img = Image.open('./static/img/waterMark.png')
        source_img.paste(logo_img, ((source_img.size[0] - logo_img.size[0])/2,
                 (source_img.size[1] - logo_img.size[1])/2), logo_img)
        markImg = source_img.tostring('jpeg', 'RGB')

        filename=  str(int(time.time())) +'.'+x.imgFile.filename.replace('\\','/').split('.')[1]

        
        ob = sae.storage.Object(markImg)
        url = saeStorage.put('wangaibing', filename, ob)
        db.insert('product', product = x.name, size = x.size,factory = x.factory,backup = x.backup,cata = x.cata,isMine = x.isMine,pic = url)
        raise web.seeother('/admin')


class checkMsg:
    def GET(self):
        checkLogin()
    	indexObj = {}
        
        if web.input():
            listQuery = "SELECT * from message  where isRead = $status  order by msgId ASC"
            msgList = db.query(listQuery,vars={'status':web.input()['status']})
        else :
            listQuery = "SELECT * from message order by msgId ASC"
            msgList = db.query(listQuery)

        if not msgList :
            indexObj['message'] = {}
            return render.checkMsg(indexObj)
        else :
            indexObj['message'] = msgList 
            return render.checkMsg(indexObj)

class readMsg :
    def POST(self):
        mid = web.data().split('=')[1]
        db.update('message', where="msgId =$mid", vars={'mid':mid},isRead = 1 )
        return 1

class readMsgAll :
    def POST(self):
        midArr = web.data().split('&')
        if midArr: 
            for mid in midArr : 
                id = mid.split('=')[1]
                db.update('message', where="msgId =$mid", vars={'mid':id},isRead = 1 )
        return 1


class login :
    def GET(self):
        ssid = hashlib.md5()
        ssid.update('jindinghengye') 
        cookie = web.cookies() 
        if  web.cookies().get('sid') and web.cookies().get('sid') == ssid.hexdigest():
            raise web.seeother('/admin')

        indexObj={}
        indexObj = {'wrong':0}
        return render.login(indexObj)

    def POST(self):
        indexObj = {}
        x = web.input()
        user = db.select('user').list()[0]
        m = hashlib.md5()
        m.update(x.password)

        if not x.username or x.username != user['name'] or not x.password or  m.hexdigest().upper() != user['pwd']:
            indexObj['wrong'] = 1
            return render.login(indexObj)
        else :
            cookie = web.cookies() 
            ssid = hashlib.md5()
            ssid.update('jindinghengye') 
            web.setcookie('sid', ssid.hexdigest(),3600)   
            raise web.seeother('/admin')
class search :
    def GET(self):
        indexObj ={}
        indexObj = {'name':'guest','path':'127.0.0.1:8080'}
        cataList = db.select('cata')
        indexObj['cata'] = cataList
        indexObj['wrong'] = 0 

        indexObj['curPage'] = web.input().get('page') and int(web.input().get('page'))+1 or 1
        offsetNum= int(indexObj['curPage']-1)*pageNum 

        plistQuery = "SELECT * from product inner join cata on product.cata=cata.cataId WHERE 1 = instr(product,$key) or  1 = instr(cataName,$key) or  1 = instr(backup,$key) or  1 = instr(factory,$key) or  1 = instr(size,$key) order by productId ASC limit $offset,$pageNum"
        productList = db.query(plistQuery,vars={'key':web.input()['skey'],'pageNum':pageNum,'offset':offsetNum})
        indexObj['pCount'] =  db.query("SELECT count(*) FROM product inner join cata on product.cata=cata.cataId WHERE 1 = instr(product,$key) or  1 = instr(cataName,$key) or  1 = instr(backup,$key) or  1 = instr(factory,$key) or  1 = instr(size,$key)",vars={'key':web.input()['skey']}).list()[0]['count(*)']

        indexObj['key'] =web.input()['skey']
        indexObj['curCata'] = 'all'
        if not productList :
            indexObj['product'] = {}
            indexObj['pCount'] = 0
            indexObj['pages'] =0
            return render.adminSearch(indexObj)
        else :
            indexObj['product'] = productList
            indexObj['pages'] = indexObj['pCount'] % pageNum and indexObj['pCount']/pageNum+1 or indexObj['pCount']/pageNum 
            return render.adminSearch(indexObj)