# MongoDBAtlas-GCP-AIML

## Background
This is a tutorial on how to use MongoDB Atlas in conjunction with Google Cloud Platform AI/ML APIs to create a event-driven model in Python.

## Setup
### MongoDB Setup
* Deploy MongoDB Atlas
* Configure Atlas username, password
* Configure Atlas network access
* Create a database called `gcpdemo` with a collection called `democol` 

### GCP Setup
* Deploy an instance
* Install python3 and git on that instance
* Clone this github repo onto that instance
* Edit `settings.cfg` with the details created in section above
* Using pip, install all requirements in `requirements.txt`
* Start the script by running `python3 runner.py`
* Ensure GCP firewall rules are set up to allow access to the default ports `8088` and `8089` or whatever you changed them to in `settings.cfg`
* Open a web browser and go to the server you deployed port `8088` and open developer console to make sure no errors. in python script window see a client is connected

## Execution
* Insert a document into the database using MongoDB Compass. 
* The document should have a field called `url` which is a full URL to an image.
* Notice that in the web page and on the CLI output of the python script that it saw an insert
* Notice that after the insert, the change stream called the Google Vision API to see what is in it