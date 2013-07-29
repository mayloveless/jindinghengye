import web
import os
import sae

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root+'/../', 'views')
render = web.template.render(templates_root,base='layout')

db = web.database(dbn='mysql', host=sae.const.MYSQL_HOST,port=int(sae.const.MYSQL_PORT),user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB)
pageNum  = 12
class index:
    def GET(self):
    	indexObj ={}
    	indexObj = {'name':'guest','path':'127.0.0.1:8080'}

    	cataList = db.select('cata')
        indexObj['cata'] = cataList
        indexObj['wrong'] = 0 

        indexObj['curPage'] = web.input().get('page') and int(web.input().get('page'))+1 or 1
        offsetNum= int(indexObj['curPage']-1)*pageNum 
        
        if web.input().get('cata'):
            
            plistQuery = "SELECT * from product inner join cata on product.cata=cata.cataId  where product.cata = $id order by productId ASC limit $offset,$pageNum"
            productList = db.query( plistQuery,vars={'id':web.input()['cata'],'pageNum':pageNum,'offset':offsetNum})
    	    indexObj['curCata']  = long(web.input()['cata'])
            indexObj['pCount'] =  db.query("SELECT count(*) FROM product where cata = $id",vars={'id':web.input()['cata']}).list()[0]['count(*)']
        else :
            
            plistQuery = "SELECT * from product inner join cata on product.cata=cata.cataId order by productId ASC limit $offset,$pageNum"
            productList = db.query(plistQuery,vars={'pageNum':pageNum,'offset':offsetNum})
            indexObj['curCata']  = 'all'
            indexObj['pCount'] =  db.query("SELECT count(*) FROM product").list()[0]['count(*)']

        if not productList :
            indexObj['product'] = {}
            indexObj['pCount'] = 0
            indexObj['pages'] = 0
            return render.product(indexObj)
        else :
            indexObj['product'] = productList
    	    indexObj['pages'] = indexObj['pCount'] % pageNum and indexObj['pCount']/pageNum+1 or indexObj['pCount']/pageNum 
    	    return render.product(indexObj)

class single :
    def GET(self, name):
    	indexObj ={}
    	indexObj = {'name':'guest','path':'127.0.0.1:8080'}
    	cataList = db.select('cata')
    	indexObj['cata'] = cataList

    	pQuery = "SELECT * from product where productId = $pid "
    	product = db.query(pQuery,vars={'pid':int(name)})
    	parr = []
    	parr =product.list()
    	
    	if  parr !=[] :
    		indexObj['product'] = parr[0]
    		indexObj['wrong'] = 0
    		indexObj['curCata']  =  parr[0].cata
    		cQuery = "SELECT * from cata where cataId = $cid "
    		curCata = db.query(cQuery,vars={'cid':indexObj['curCata']})[0]
    		indexObj['curCataName'] = curCata.cataName
    		return render.single(indexObj)
    	else :
            indexObj['product'] = ''
            indexObj['curCataName'] = ''
            indexObj['wrong'] = 1
            indexObj['curCata']  = 'all'
            return render.single(indexObj)

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
        if not productList :
            indexObj['product'] = {}
            indexObj['pCount'] = 0
            indexObj['pages'] =0
            return render.search(indexObj)
        else :
            indexObj['product'] = productList
            indexObj['pages'] = indexObj['pCount'] % pageNum and indexObj['pCount']/pageNum+1 or indexObj['pCount']/pageNum 
            return render.search(indexObj)

class patent :
    def GET(self):
        indexObj ={}
        indexObj = {'name':'guest','path':'127.0.0.1:8080'}

        plistQuery = "SELECT * from product inner join cata on product.cata=cata.cataId WHERE isMine =1 order by productId ASC "
        productList = db.query(plistQuery)
        if not productList :
            indexObj['product'] = {}
            return render.patent(indexObj)
        else :
            indexObj['product'] = productList
            return render.patent(indexObj)

