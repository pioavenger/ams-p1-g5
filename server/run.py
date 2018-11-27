import os
import cherrypy

class app(object):

    def __init__(self):
        pass

    @cherrypy.expose
    def signup(self,username):
        pass

    @cherrypy.expose
    def signin(self,username):
        pass

    @cherrypy.expose
    def signout(self,username):
        pass

    @cherrypy.expose
    def browse(self,username):
        pass

    @cherrypy.expose
    def book(self,username):
        pass


config={
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
}

cherrypy.config.update({'server.socket_host': 'localhost',
                        'server.socket_port': 8000,
                       })

cherrypy.quickstart(app(), "/",config)
