import os

import sae
import web
import app.controllers
       
urls = (
    '/', 'app.controllers.static.index',
    '/about','app.controllers.static.about',
    '/contact','app.controllers.static.contact',
    '/partner','app.controllers.static.partner',
    '/message','app.controllers.message.index',
    '/product','app.controllers.product.index',
    '/patent','app.controllers.product.patent',
    '/product/(\d+)','app.controllers.product.single',
    '/product/search','app.controllers.product.search',
    '/login','app.controllers.admin.login',
    '/admin/search','app.controllers.admin.search',    
    '/admin','app.controllers.admin.index',
    '/admin/add','app.controllers.admin.add',
    '/admin/edit','app.controllers.admin.edit',
    '/admin/checkMsg','app.controllers.admin.checkMsg',
    '/admin/read','app.controllers.admin.readMsg',
    '/admin/readAll','app.controllers.admin.readMsgAll',
    '/admin/del','app.controllers.admin.delete',
    '/ustblib','app.controllers.tool.ustblib',
    '/if13sis','app.controllers.tool.if13sis',
    '/get_token','app.controllers.tool.getToken',
    '/tools','app.controllers.tool.index',
    '/weixin','app.controllers.weixin.index'
)

app = web.application(urls, globals()).wsgifunc()

application = sae.create_wsgi_app(app)