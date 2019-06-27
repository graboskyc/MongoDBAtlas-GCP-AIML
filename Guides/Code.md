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
  pip install tornado dnspython pymongo google-cloud-vision
```

* The packages are used for (respectively): a python webserver, allow the use of MongoDB SRV connection strings, connect to MongoDB databases, and connect to the GCP Vision API
* create a directory called `example` and then `cd example`

## Create your GCP credential store
* Take the JSON credential file you downloaded earlier from GCP and copy the contents
* Using the text editor of your choice, create a file called `gcpcreds.json` and paste in the contents and save it

## Creating the sample python script
Using the text editor of your choice, create a `runner.py` with the simplified contents as below:

At the top we start with our imports:

```
import pymongo
from bson.objectid import ObjectId
import os
from bson.json_util import dumps
from google.cloud import vision
import json
```

To review these imports, `pymongo` is the official MongoDB driver for python, we need the `bson` line to convert the string version of a ObjectID to the `ObjectID` datatype found in the [BSON spec](http://bsonspec.org/) and to quickly dump the output to strings, `json` is used to parse JSON, and then the official library for communicating with the GCP Vision API is used.

After that is there, let's put our global configuration and modify it with your MongoDB Python connection string:

```
# configure connection to mongodb
conn = pymongo.MongoClient("INSERT YOUR MONGODB CONNECTION STRING HERE")
handle = conn["gcpdemo"]["democol"]

# configure connection to gcp vision api
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcpcreds.json"
gcpapi = vision.ImageAnnotatorClient()
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
```

That last piece just prints the data out on the command line.

This is meant to be a simple illustration of how this works. Security is bypassed and this will not scale well. However with this knowledge, you can build applications using these features.

Note that Python is very particular about white space, so as you copy/paste, make sure that your tabs are all even.

## Running the aplication
Once that is saved, run the application:
* `python3 runner.py`
* Insert a document into the database using MongoDB Compass or the new Data Explorer view in MongoDB Atlas which you can get to via the "Collections" button. The document you insert should have a field called `url` which is a full URL to an image.
* Notice that in the CLI output of the python script that it saw an insert
* Notice that after the insert, the change stream called the Google Vision API to see what is in it. Refresh the Compass or Atlas Data Explorer view and see the rich data structure of the GCP Vision API.
