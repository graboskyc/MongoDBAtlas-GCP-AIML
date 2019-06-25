import pymongo
import tornado.ioloop                                                                                                                                                                                       
import tornado.web                                                                                                                                                                                          
import tornado.websocket
import threading
import os
from bson.json_util import dumps
import configparser

# global variables
_WEBSETTINGS = { "static_path": os.path.join(os.path.dirname(__file__)+"Web/", "static") }
_clients = []

# get config file settings
cfg = configparser.ConfigParser()
cfg.read('settings.cfg')

# configure connection to mongodb
conn = pymongo.MongoClient(cfg['DEFAULT']['_URI'])
handle = conn[cfg['DEFAULT']['_DBNAME']][cfg['DEFAULT']['_COLNAME']]

#########
# configure web interface
#########
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("Web/index.html", title="Welcome")

class WebSockHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("New client connected")
		#_clients.append({"id":self.client_id, "ws":self})
		_clients.append(self)
		self.write_message("You are connected")

	def on_message(self, msg):
		print(msg)
		self.write_message(msg)

	def on_close(self):
		#i = 0
		#for c in _clients:
		#	if(c["id"] == self.client_id):
		#		_clients.pop(i)
		#	i = i + 1
		print("Client disconnected")

	def check_origin(self, origin):
		# who cares about security
		return True


###########
# Main loop
##########
if __name__ == "__main__":
	# start up the web servers as tornado applications
	application = tornado.web.Application([(r"/", MainHandler),], **_WEBSETTINGS)
	appsoc = tornado.web.Application([(r"/", WebSockHandler),],)

	# start a web server for sockets
	appsoc.listen(cfg['DEFAULT']['_WEBSOCKPORT'])

	# start a web server for index.html and run in background thread
	application.listen(cfg['DEFAULT']['_WEBPORT'])
	t = threading.Thread(target=tornado.ioloop.IOLoop.instance().start)
	t.daemon = True
	t.start()

	# connect to a change stream
	change_stream = handle.watch()
	# every change send to client
	for change in change_stream:
		for c in _clients:
			print(dumps(change))
			print("")
			c.write_message(dumps(change))
