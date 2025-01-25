from openstackPythonCmd.openmobile import *
from utils.app import app
from openstackPythonCmd.openstackcmd import *
from openstackPythonCmd.openmobile import *
from flask_cors import CORS,cross_origin


CORS(app, resources={r"/*": {"origins": "*"}})
# -------------------- OpenStack Basic Commands Routes --------------------
# -------------------- Get Commands -------------------- 
@app.route('/api/getserverdetails', methods=['POST'])
def getserverdetails():
    return OpenStackCMD.getServerDetails()

@app.route('/api/getservernamelist', methods=['GET'])
def getservernamelist():
    return OpenStackCMD.getServerNameList()

@app.route('/api/getimagelist', methods=['POST'])
def getimagelist():
    return OpenStackCMD.getImageList()

@app.route('/api/getflavorlist', methods=['POST'])
def getflavorlist():
    return OpenStackCMD.getFlavorList()

@app.route('/api/getnetworkdetails', methods=['POST'])
def getnetworklist():
    return OpenStackCMD.getNetworkDetails()

@app.route('/api/getnetworknamelist', methods=['GET'])
def getnetworknamelist():
    return OpenStackCMD.getNetworkNameList()

# -------------------- Find Commands --------------------
@app.route('/api/findserver', methods=['GET'])
def findserver():
    return OpenStackCMD.findServer()

@app.route('/api/findimage', methods=['GET'])
def findimage():
    return OpenStackCMD.findImage()

@app.route('/api/findflavor', methods=['GET'])
def findflavor():
    return OpenStackCMD.findFlavor()

@app.route('/api/findnetwork', methods=['GET'])
def findnetwork():
    return OpenStackCMD.findNetwork()

# -------------------- OpenStack Follower Command Routes -------------------- 
@cross_origin(origins=["http://localhost:3000"])
@app.route('/api/createfollowerserver', methods=['POST'])
def createfollowerserver():
    return createFollowerServerUsingCLI()

# -------------------- Delete Command -------------------- 
@app.route('/api/deleteserver', methods=['POST'])
def deleteserver():
    return deleteCreatedInstance()

@app.route('/api/deleteableinstancelist', methods=['GET'])
def deleteableinstancelist():
    return OpenStackCMD.deleteableInstanceList()

