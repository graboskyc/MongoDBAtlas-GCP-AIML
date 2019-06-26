# Writing the code
You can use the completed code located in the `FinishedSampleCode` if you want. However if you want to learn the process for writing it, follow along here.

## Pre-reqs
* Have the GCP instance deployed already
* Have the GCP Vision API enabled
* Have MongoDB Atlas deployed
* Instead of running the commands to clone this repo there, we will write it from scratch using the GCP CloudShell

## Preparing the GCP Instance
* You should have already deployed the instance running Ubuntu. If you chose a different distribution, note that this will still work but the following commands may differ
* Run the following commands to install python and python prereqs

```
  sudo apt-get update
  sudo apt-get install python3-pip
  pip install tornado dnspython pymongo configparser google-cloud-vision
```
* The packages are used for (respectively): a python webserver, allow the use of MongoDB SRV connection strings, connect to MongoDB databases, parse config files, and connect to the GCP Vision API
* create a directory called `example` and then `cd example`

## Creating a basic HTML File
Using the text editor of your choice, create a `index.html` with the simplified contents as below:

```
<html><head>
  <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>

  <script type="text/javascript">
    $(document).ready(function() {
      var localip = window.location.hostname;
      var connection = new WebSocket('ws://' + localip + ":8089");
      connection.onmessage = function (event) {
        console.log(event);
        var mdbmsg = JSON.parse(event.data);
        var html = "<p><code>"+JSON.stringify(mdbmsg)+"</code></p><hr />"
        $('#div_msg').prepend(html);
      }
      $("#btn_insert").click(function(){
        connection.send($('#txt_url').val());
        $('#txt_url').val('');
      }); 
    });
  </script>
</head><body>
      <h1>Here's My Change Stream!</h1>
      <h3>Newest events on top</h3>
      <hr />
      <div style="height:75px;">
        <input type="text" id="txt_url" /> <button id="btn_insert">Insert</button>
      </div>
      <hr />
      <div id="div_msg"></div>
    </div>
</body></html>
```

To review this code, it is a simple HTML page that uses Jquery to simplify some JavaScript work. It opens a websocket to the same server this is running on port 8089 and will take whatever it recieves and putting it in the container called `div_msg`. There is also a basic text box that when the button is clicked, it will send that (a URL) over the websocket back to the server.

## Create your GCP config store
* Take the JSON credential file you downloaded earlier from GCP and copy the contents
* Using the text editor of your choice, create a file called `gcpcreds.json` and paste in the contents and save it

## Creating the sample python script
Using the text editor of your choice, create a `runner.py` with the simplified contents as below:

At the top we start with our imports:

```
import pymongo
from bson.objectid import ObjectId
import tornado.ioloop                                                                                                                                                                                       
import tornado.web                                                                                                                                                                                          
import tornado.websocket
import threading
import os
from bson.json_util import dumps
from google.cloud import vision
import json
```

After that is there, let's put our global configuration and modify it with your MongoDB Python connection string

```
# global variables
_WEBSETTINGS = { }
_clients = []

# configure connection to mongodb
conn = pymongo.MongoClient("INSERT YOUR MONGODB CONNECTION STRING HERE")
handle = conn["gcpdemo"]["democol"]

# configure connection to gcp vision api
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcpcreds.json"
gcpapi = vision.ImageAnnotatorClient()
```

Next we create the boilerplate code to create a webserver in python using tornado:

```
#########
# configure web interface
#########
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html", title="Welcome")

class WebSockHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("New client connected")
		_clients.append(self)
		self.write_message("You are connected")

	def on_message(self, msg):
		print(msg)
		handle.insert_one({"url":msg})

	def on_close(self):
		print("Client disconnected")

	def check_origin(self, origin):
		return True
```

Next is the main loop. We start by starting the web server itself

```
# start up the web servers as tornado applications
application = tornado.web.Application([(r"/", MainHandler),], **_WEBSETTINGS)
appsoc = tornado.web.Application([(r"/", WebSockHandler),],)

# start a web server for sockets
appsoc.listen(8089)

# start a web server for index.html and run in background thread
application.listen(8088)
t = threading.Thread(target=tornado.ioloop.IOLoop.instance().start)
t.daemon = True
t.start()
```

Then is connecting to a MongoDB Change Stream. This opens a listener on the collection and will get a notification of every insert, update, delete, and replace. Here we care about an insert and make sure that insert has a `url` attribute. If it does, it sends the URL to the GCP Vision API and then takes the response and updates the MongoDB Document.

You can learn more about the [MongoDB Change Streams by clicking here](https://docs.mongodb.com/manual/changeStreams/).

```
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
            resp = gcpapi.label_detection(image=image)

            # odd formatting i dont have time for right now so just process it first
            labels = []
            for label in resp.label_annotations:
                obj = {}
                obj['description'] = label.description
                obj['score'] = label.score
                labels.append(obj)

            # update mongodb record with response from GCP
            handle.update_one({'_id':ObjectId(change["fullDocument"]["_id"])}, {"$set": {"gcpvisionlabels":labels}})

    # print to screen
    print(dumps(change))
    print("")

    for c in _clients:
        # fix disconnecting clients symptom rather than fixings
        try:
            c.write_message(dumps(change))
        except:
            pass

```

That last piece just prints the data out the web socket to the web page as well as the output of the python script on the command line.

This is meant to be a simple illustration of how this works. Security is bypassed and this will not scale well. However with this knowledge, you can build applications using these features.

## Running the aplication
Once that is saved, run the application:
* `python3 runner.py`
* Open a web browser to the GCP instance running on port 8088 over http
* Insert a document into the database using MongoDB Compass or the new Data Explorer view in MongoDB Atlas which you can get to via the "Collections" button. The document you insert should have a field called `url` which is a full URL to an image.
* Alternately enter the URL into the web page directly and press the green "Insert" button
* Notice that in the web page and on the CLI output of the python script that it saw an insert
* Notice that after the insert, the change stream called the Google Vision API to see what is in it. Refresh the Compass or Atlas Data Explorer view and see the rich data structure of the GCP Vision API.
