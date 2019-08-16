# GCP Instance Setup
* Create a micro Ubuntu 19.04 GCE VM instance in us-east4 using the instructions given here [link](https://www.google.com/url?q=https://cloud.google.com/compute/docs/quickstart-linux&sa=D&ust=1560383195254000)

![](images/newss04.png)

* In the search box at the top, enter “Firewall” and select the matching suggestion "Firewall Rules VPC network”

![](images/image19.png)

* Click “Create Firewall Rule” at the top to create a new rule to open up the needed port for our new server

![](images/image18.png)

* Enter the following details and click “Create”:
```
Name: gcpatlasdemo
Targets: All instances in the network
Source IP ranges:  0.0.0.0/0
Protocols and ports:  
    tcp: 8088-8089
``` 
![](images/newss05.png)

* [Make sure to do the API Vision setup](GCPVisionSetup.md)

* Go back to the Compute Engine page to list all VM instances.

![](images/image27.png)

* After your instance is created, SSH to your instance by clicking on the SSH button of your instance.

![](images/image16.png)

* You should see a CloudShell window similar to this open...

![](images/image7.png)

* Run the following commands:

```
  sudo apt-get update
  sudo apt-get install -y python3-pip
  sudo apt-get install -y git
  git clone https://github.com/graboskyc/MongoDBAtlas-GCP-AIML.git
  cd MongoDBAtlas-GCP-AIML/FinishedSampleCode
  python3 -m pip install -r requirements.txt
```

* Edit the `gcpcreds.json` to have the credentials of the json file you downloaded above
* Edit `settings.cfg` to have the Atlas connection string created above
* Run `python3 runner.py` to start the application
* Visit the URL of your server port 8088 and you should see a web page
  * e.g. if the public IP address of your Google Cloud instance is 12.23.45.56, open a browser and visit http://12.23.45.56:8088

![](images/newss02.png)
