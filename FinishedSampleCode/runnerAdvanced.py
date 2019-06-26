import pymongo
from bson.objectid import ObjectId
import tornado.ioloop
import tornado.web
import tornado.websocket
import threading
import os
from bson.json_util import dumps
import configparser
from google.cloud import vision
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import json
from datetime import datetime

# This is the same as the basic runner but it also uses the Language API to do sentiment analysis.
# So if you want to use this one, enable that API as well in the GCP console.

# global variables
_WEBSETTINGS = { "static_path": os.path.join(os.path.dirname(__file__)+"Web/", "static") }
_clients = []

# get config file settings
cfg = configparser.ConfigParser()
cfg.read('settings.cfg')

# configure connection to mongodb
conn = pymongo.MongoClient(cfg['DEFAULT']['_URI'])
handle = conn[cfg['DEFAULT']['_DBNAME']][cfg['DEFAULT']['_COLNAME']]

# configure connection to gcp vision api
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcpcreds.json"
gcpvision = vision.ImageAnnotatorClient()
gcplang = language.LanguageServiceClient()

#########
# configure web interface
#########
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("Web/index.html", title="Welcome")

class WebSockHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("New client connected")
		_clients.append(self)
		self.write_message("You are connected")

	def on_message(self, msg):
		print(msg)
		#self.write_message(msg)
		# oh man this is bad practice
		if msg.startswith("http"):
			handle.insert_one({"url":msg, "created":datetime.now()})
		else:
			handle.insert_one({"text":msg, "created":datetime.now()})

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
	# every change in the db
	for change in change_stream:
		# can be insert, update, replace (Compass)
		if change["operationType"] == "insert":
			# make sure it had a URL attribute
			if "url" in change["fullDocument"]:
				# boilerplate to prep gcp api request
				image = vision.types.Image()
				image.source.image_uri = change["fullDocument"]["url"]
				resp = gcpvision.label_detection(image=image)

				# odd data type i dont have time for right now so just process it first
				labels = []
				for label in resp.label_annotations:
					obj = {}
					obj['description'] = label.description
					obj['score'] = label.score
					labels.append(obj)

				# update mongodb record with response from GCP
				handle.update_one({'_id':ObjectId(change["fullDocument"]["_id"])}, {"$set": {"gcpvisionlabels":labels}})

			if "text" in change["fullDocument"]:
				# boilerplate to prep gcp api request
				textToCheck = types.Document(content=change["fullDocument"]["text"], type=enums.Document.Type.PLAIN_TEXT)
				annotations = gcplang.analyze_sentiment(document=textToCheck)

				# odd data type i dont have time for right now so just process it first
				sentiment = {}
				sentiment['score'] = annotations.document_sentiment.score
				sentiment['magnitude'] = annotations.document_sentiment.magnitude
				sentiment['lang'] = annotations.language
				sentiment['sentences'] = []

				for index, sentence in enumerate(annotations.sentences):
					s = {}
					s['index'] = index
					s['sentence'] = sentence.text.content
					s['offset'] = sentence.text.begin_offset
					s['score'] = sentence.sentiment.score
					sentiment['sentences'].append(s)

				# update mongodb record with response from GCP
				handle.update_one({'_id':ObjectId(change["fullDocument"]["_id"])}, {"$set": {"gcplanguage":sentiment}})

		# print to screen
		print(dumps(change))
		print("")

		for c in _clients:
			# fix disconnecting clients symptom rather than fixings
			try:
				c.write_message(dumps(change))
			except:
				pass
