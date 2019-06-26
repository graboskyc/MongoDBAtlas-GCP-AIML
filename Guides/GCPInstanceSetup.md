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

* In the top box, search for "Credentials" and choose the auto-complete option 

* In the search field up top, enter “compute engine” and select the suggestion: "Credentials APIs & Services"

* Click the blue "Create credentials" then choose "Service account key" in the list 

* Choose "new service account" and give it a name like atlasgcpdemo. For the scope, choose *what should i choose here?* and JSON format. Save and it will download the JSON file. Keep these contents for later.

* Go back to the Compute Engine page to list all VM instances.

![](images/image27.png)

* After your instance is created, SSH to your instance by clicking on the SSH button of your instance.

![](images/image16.png)

* You should see a CloudShell window similar to this open...

![](images/image7.png)

* Run the following commands:

```
  sudo apt-get update
  sudo apt-get install python3-pip
  git clone https://github.com/graboskyc/MongoDBAtlas-GCP-AIML.git
  cd MongoDBAtlas-GCP-AIML/FinishedSampleCode
  pip install -r requirements.txt
```

* Edit the `gcpcreds.json` to have the credentials of the json file you downloaded above
* Edit `settings.cfg` to have the Atlas connection string created above
* Run `python3 runner.py` to start the application
* Visit the URL of your server port 8088 and you should see a web page

![](images/newss02.png)