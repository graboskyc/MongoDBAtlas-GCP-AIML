# MongoDBAtlas-GCP-AIML

## Background
This is a tutorial on how to use MongoDB Atlas in conjunction with Google Cloud Platform AI/ML APIs to create a event-driven model in Python.

This is part of a workshop series presented by MongoDB and Google Cloud. However it can also be done on its own.

### Technical Complexity

_Beginner_

### Duration

_45 Minutes_

## Setup
### MongoDB Setup
* Create a free account on MongoDB Atlas on [cloud.mongodb.com](https://cloud.mongodb.com) Click on “Try Free”at the top right if you do not have an account or “Sign In” if you already have a login. 

![](images/image1.png)

* Once on the MongoDB Atlas Homepage, select “Build a Cluster”

![](images/imageXX.png)

* Create New Cluster by selecting Google Cloud Platform as a “Cloud Provider” and leave all other settings as-is and click "Create Cluster" on the bottom right to deploy your M0 (free) cluster

* While this spins up, lets click on the “Database Access” submenu, under “Security” on the left menu. 

![](images/image33.png)

* Click the “Add New User” button on top right

![](images/image24.png)

* Enter a user name. For our demo, let’s enter `mdbadmin` and enter a secure password.  Record your user name and password in a safe location for reference later. Under “User Privileges”, select “Atlas admin” and click on the “Add User button to complete this section.

![](images/image9.png)

* Lets click on the “Network Access” submenu, under “Security” on the left menu. Click on “Add IP Address”.

![](images/image39.png)

* Select “Allow Access from Anywhere” for the purpose of this demo and click on “Confirm”.  

*Note*:  When actually putting something into production, you will want to narrow the scope of where your database can be accessed and specify a specific IP address/CIDR block.

![](images/image4.png)

* Go to “Clusters” submenu, under “Atlas” on the left menu. 

* Click on the "Collections" button and create a database called `gcpdemo` with a collection called `democol` 

* Go to “Clusters” submenu, under “Atlas” on the left menu. 

* Click on “Connect” button. A window will open. Select “Connect Your Application.” Choose Python and copy the connection string they give you. We will need this later.


### GCP Vision API Setup
![](images/newss01.png)

* Go to cloud.google.com and login with your Google account. If you don't have a Google account, please create a free trial account by following instructions at this [link](https://console.cloud.google.com/freetrial).

* If not already there, go to https://console.cloud.google.com/

* Create a new project, by selecting the following dropdown in the top left:

![image](images/image30.png)

* A new window will pop up.  In it, select "New Project" in the top right:

![image](images/image14.png)

* Give your Vision API demo a new project name.  Let's go with “mongodb-vision-demo” and click the “Create” button:

![image](images/image28.png)

![image](images/image31.png)

* After your new project is done being created. Go back to the dropdown from before and select your new project name:

![image](images/image22.png)

* When the right project is selected, the name will change to reflect this in the dropdown in the top left of your console:

![image](images/image5.png)

* Get a credential and put it in `gcpcreds.json`

### GCP Instance Setup
* Create a Debian Linux GCE VM instance using the instructions given here [link](https://www.google.com/url?q=https://cloud.google.com/compute/docs/quickstart-linux&sa=D&ust=1560383195254000)

![](images/image3.png)

* In the search box at the top, enter “Firewall” and select the matching suggestion”Firewall rules”under “VPC network”

![](images/image19.png)

* Click “Create Firewall Rule” at the top to create a new rule to open up the needed port for our new server

![](images/image18.png)

* Enter the following details and click “Create”:
```
Name: port8088
Targets: All instances in the network
Source IP ranges:   [your specific source IP / range]  
Protocols and ports:  
    tcp: 8088
``` 
![](images/image38.png)

* Repeat above for port 8089

* In the search field up top, enter “compute engine” and select the suggestion:

![](images/image27.png)

* After your instance is created, SSH to your instance by clicking on the SSH button of your instance.

![](images/image16.png)

* You should see a CloudShell window similar to this open...

![](images/image7.png)

* Run `git clone https://github.com/graboskyc/MongoDBAtlas-GCP-AIML.git`
* cd to that directory
* `pip install requirements.txt`
* Edit the `gcpcreds.json` to have the credntials created above
* Edit `settings.cfg` to have the Atlas connection string created above
* `python runner.py`
* Visit the URL of your server port 8088 and you should see a web page

![](images/newss02.png)

## Execution
* Insert a document into the database using MongoDB Compass or the new Data Explorer view in MongoDB Atlas which you can get to via the "Collections" button. The document you insert should have a field called `url` which is a full URL to an image.
* Alternately enter the URL into the web page directly and press the green "Insert" button
* Notice that in the web page and on the CLI output of the python script that it saw an insert
* Notice that after the insert, the change stream called the Google Vision API to see what is in it. Refresh the Compass or Atlas Data Explorer view and see the rich data structure of the GCP Vision API.
![](images/newss03.png)

## Extra Credit
* Create a GCP Cloud Storage Bucket to host your own images

## Sample Data
Feel free to use the following URLs for execution:
1. https://storage.googleapis.com/demo-visionapi-atlas/StatueofLiberty.jpeg
2. https://storage.googleapis.com/demo-visionapi-atlas/crash1.jpg
3. https://storage.googleapis.com/demo-visionapi-atlas/nike_logo_30021.jpg
4. https://storage.googleapis.com/demo-visionapi-atlas/Marketing/eiffel-tower.jpg
5. https://storage.googleapis.com/demo-visionapi-atlas/Finance/check.jpg
