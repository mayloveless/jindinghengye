import web
import os
import sae
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root+'/../', 'views')
render = web.template.render(templates_root,base='layout')

class index:
    def GET(self):
    	indexObj = {'name':'guest','path':'127.0.0.1:8080'}
        return render.index(indexObj)


class about:
    def GET(self):
    	
        return render.about()


class contact:
    def GET(self):
    	
        return render.contact()

class partner:
    def GET(self):
    	indexObj = {'name':'guest','path':'127.0.0.1:8080'}
        return render.partner(indexObj)


       
            
