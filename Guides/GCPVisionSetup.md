# GCP Vision API Setup

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

* In the search box, search for "Cloud Vision API" and choose that option in the drop down

![](images/newss06.png)

* Enable the API

![](images/newss01.png)

* Create a credential of type "Service Account Key" with a name of your choosing, Key Type is JSON, and Role of ******** - _what is the minimum here_?

![](images/newss07.png)

* When saving, it will download the JSON file. Read its contents put it in `gcpcreds.json`