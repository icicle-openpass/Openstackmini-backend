from flask import jsonify, request
from openstack import connection
from openstackPythonCmd.openstackcmd import OpenStackCMD
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

def createFollowerServer():
    # Create a connection with Jet2Stream
    creds_conn = connection.Connection(cloud='CIS220074_IU')

    # Parameters required to create a virtual machine
    # ``` API REST FORMAT
    # {
    #     "image_id":"",
    #     "flavor":"",
    #     "network":"",
    #     "type":"",
    #     "port":"",
    #     "leader_ip":"",
    #     "security_group":""
    #     "namespace":""
    # }
    data = request.json
    print(data)
    # instname = "ICICLE_Follower_Node_Namespace_" + data["namespace"]
    instname = "OpenStack_Mini"
    image = data["image_id"]
    flavor = data["flavor"]
    network = data["network"]
    typeof = data["type"]
    security_group = data["security_group"]

    # Find all the above parameter and fetch the data
    find_image = OpenStackCMD.findImage(image)
    find_server = OpenStackCMD.findServer(instname)
    find_flavor = OpenStackCMD.findFlavor(flavor)
    find_network = OpenStackCMD.findNetwork(network)

    # Check if the instance exist. If yes then delete it, just to start from start
    if find_server: # Checking if server exist or not
        return jsonify("Server Already Exits"),404

    # Below are the process to create a virtual machine on Jet2Stream
    # Create instance --> Find "Public Network" --> Create public ip in "Public Network" --> Get the list of Ports --> Update the instance & networks IP table
    # Create a new instance
    create_server = OpenStackCMD.createServer(instname,find_image.id,find_flavor.id,[{"uuid": find_network.id}],[{"name": security_group}])

    # Wait for server creation and get the server info
    server_confirm = creds_conn.compute.wait_for_server(create_server)
    print(f"Server {server_confirm.name} is active with ID {server_confirm.id}")

    # Fetch the data on "Public" network and then create the floating IP
    public_network = OpenStackCMD.findNetwork("public")
    floating_ip = OpenStackCMD.createIP(public_network.id)
    print(f"Allocated Floating IP: {floating_ip.floating_ip_address}")

    # Get the list of ports of that particular server
    server_ports = list(creds_conn.network.ports(device_id=server_confirm.id))
    if not server_ports:
        raise Exception("No network ports found for the server.")

    # Fetch the first port
    server_port = server_ports[0]
    print(f"Found Server Port: {server_port.id}")

    # Update the IP in that partiular server.
    creds_conn.network.update_ip(floating_ip, port_id=server_port.id)
    print(f"Floating IP {floating_ip.floating_ip_address} assigned to server {server_confirm.name}")

    # Get server's private addresses
    get_server_details = server_confirm.addresses
    inst_pvt_ip =  get_server_details['digitalagci'][0]['addr']

    # Response
    return jsonify({
        "server_name": server_confirm.name,
        "server_id": server_confirm.id,
        "server_network_name":find_network.name,
        "server_network_id": find_network.id,
        "server_flavor":find_flavor.name,
        "server_image":find_image.id,
        "server_public_ip": floating_ip.floating_ip_address,
        "server_private_ip":inst_pvt_ip,
        "server_port":server_port.id,
        "server_status":server_confirm.status,
        "server_log_checking_time": 10
    }),200


def createFollowerServerUsingCLI():
    data = request.json

    # Parameters required to create a virtual machine
    # ``` API REST FORMAT
    # {
    #     "name":"",
    #     "image_id":"",
    #     "flavor":"",
    #     "network":"",
    #     "security_group":""
    # }
    instname = data["name"]
    image = data["image_id"]
    flavor = data["flavor"]
    network = data["network"]
    security_group = data["security_group"]

    print(data)

    # Cloud Creds to Create the VM
    cred_path = "./utils/creds/rc.sh"
    cred_cmd = f"bash -c 'source {cred_path} && env'"
    creds = subprocess.run(cred_cmd, capture_output=True, executable="/bin/bash", text=True, check=True, shell=True)

    if creds.returncode != 0:
        print("Error sourcing RC file:", creds.stderr)
        exit(1)

    env_vars = {}
    for line in creds.stdout.split("\n"):
        if "=" in line:
            key, value = line.split("=", 1)
            env_vars[key] = value

    os.environ.update(env_vars)

    # Create Virtual Machine
    create_inst_cmd = ["openstack", "server", "create", "--image", str(image), "--network", str(network), "--security-group", str(security_group), "--flavor", str(flavor), str(instname)]
    subprocess.run(create_inst_cmd, capture_output=True, text=True)

    # Create Public IP
    create_public_ip = ["openstack", "floating", "ip", "create", "public", "-f", "value", "-c", "floating_ip_address"]
    create_publicip_result = subprocess.run(create_public_ip, capture_output=True, text=True)

    if create_publicip_result.returncode != 0:
        print("Error creating floating IP:", create_publicip_result.stderr)
        exit(1)

    public_ip = create_publicip_result.stdout.strip()

    # Link Public IP to Server
    connect_to_server = ["openstack", "server", "add", "floating", "ip",  str(instname), str(public_ip)]
    subprocess.run(connect_to_server, capture_output=True, text=True)

    response =  jsonify({
        f"{str(instname)}_access_ip": public_ip,
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def deleteCreatedInstance():
    data = request.json
    creds_conn = connection.Connection(cloud="CIS220074_IU")
    # Parameters required to delete a virtual machine
    # ``` API REST FORMAT
    # {
    #     "instname":"",
    #     "floatingip":"",
    # }
    instname = str(data["resourcename"])

    servers = creds_conn.compute.servers()
    filtered_server = None

    for server in servers:
        if server.name == instname:
            filtered_server = server
            break

    server_id = filtered_server.id
    floating_ip = filtered_server.addresses['digitalagci'][1]['addr']
    delete_float_ip = ["openstack", "floating", "ip", "delete", str(floating_ip)]
    delete_floating_ip = subprocess.run(delete_float_ip, capture_output=True, text=True)
    delete_server_ip = creds_conn.compute.delete_server(server_id)
    return jsonify({
        "Message": f"Instance '{instname}' deleted successfully with access ip '{str(floating_ip)}'"
    })