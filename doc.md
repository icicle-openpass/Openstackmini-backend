# 💻 -> ☁️ Edge2Clouds Documentation 💻 -> ☁️

This is a REST API which is developed in python langauage using flask framework.

To get started wih the project installation have a look at the folder structure:

```
Edgedeviceflask
    |
    |-  openstackPythonCmd
    |    |-  cluster.py
    |    |-  twin.py
    |    |-  openstackcmd.py
    |
    |-  utils
    |    |-  app.py
    |    |-  cred.py
    |
    |-  .env
    |-  main.py
    |-  app.py
    |-  requirements.txt
    |-  routes.py
```

## ⚙️ Setup ⚙️

To get started with the setup:
1) Make sure to be in the same directory in terminal
2) Make sure you have proper python version. Project was developed in python 3.10.12
3) Make sure you have pip installed in you system. Project was developed using pip 22.0.2
4) Now, we will install all the libraries using the file `requirements.txt`.<br>
   ```bash 
    pip3 install -r requirements.txt 
    ```
5) Now to run the project we will run the main.py.<br>
    ```bash 
    python3 main.py 
    ```
    Note: Warning! Don't use command `flask run`. It won't work because we have made sure that each component and files are executed independently.
6) Go to http://127.0.0.1:5000/. This is the base URL.
7) ⚠️**Wait!!** The API won't run because we haven't setup the cloud config file.
8) Go to 📁utils --> clouds.yaml. Copy this file to ```.config``` folder.
9) Remember to create a folder name ```openstack``` and then copy ```clouds.yaml``` inside that folder.
10) Now you are good to go with the running of project.

## 📁 File Structure 📁
- **cluster.py, twin.py and openstackcmd.py** <br>
    - There are classes created and the functions for each openstack functionality.
    - We call those function from that particular class which makes us sure that we are accessing only that particular class while execution.
    - Reason for not creating multiple files for each functionality is that it will help us from scalability point of view as the project grows.

- **main.py**<br>
    - Its CORS enabled and specifically hosted on 0.0.0.0:5000 to make sure that whenever we run this project on any cloud instance it can be easily access using `cloud_ip:5000`.
    - All local varible like .env are executed inside the main.py to make sue they are loaded inside the application perfectly.

- **routes.py**<br>
    - The particular pattern is followed in this file. The path `/xyz` is same as the function name. But the function which it returs follows the Camel-Case.

## 🌐 API Routing Functionality 🌐

####   🔗 Route : '/'
Functionality : This function return the "Welcome to Icicle Edge to Cloud"

####   🔗 Route : '/getcreds'
**Functionality** : This function makes sure to send the authentication parameter to the jet2stream cloud using openstack.<br>
**Output** : Nothing! All process happen in backend and the creds are fetched for local .env files which makes sure that the data is not visible on client side.

####   🔗 Route : '/getserverlist'
**Functionality** : This function helps us to get the all the data realted to the servers. This will let us know that how many servers are created and what type of server are created.<br>
**Output** : JSON 