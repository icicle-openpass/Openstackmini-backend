from flask import jsonify, request
from openstack import connection
from dotenv import load_dotenv
import os

load_dotenv()

class OpenStackCMD:

    # Get Utilities
    def getServerDetails():
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        data = request.json
        try:
        # List all servers and filter by the given server name
            servers = creds_conn.compute.servers()
            filtered_server = None
            name = data['resourcename']

            for server in servers:
                if server.name == name:
                    filtered_server = server
                    break  # Stop once we find the matching server

            # If server is found, return its details
            if filtered_server:
                server_details = {
                    "name": filtered_server.name,
                    "id": filtered_server.id,
                    "status": filtered_server.status,
                    "flavor": filtered_server.flavor['name'],
                    "image": filtered_server.image.id,
                    "addresses": filtered_server.addresses
                }
                return jsonify(server_details), 200
            else:
                return jsonify({"error": "Server not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500 
    
    def getServerNameList():
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        server_list = []
        for server in creds_conn.compute.servers():
            server_list.append(server.name)

        return jsonify(server_list),200
    
    def getImageList():
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        images_list = []
        for images in creds_conn.compute.images():
            images_list.append({
                "id": images.id,
                "name": images.name,
                "status": images.status,
            })
            
        return jsonify(images_list),200
    
    def getFlavorList():
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        flavors_list = []
        for flavor in creds_conn.compute.flavors():
            flavors_list.append({
                "id": flavor.id,
                "name": flavor.name,
                "ram": flavor.ram,
                "disk": flavor.disk,
                "extra_specs": flavor.extra_specs,
                "location": flavor.location,
            })
            

        return jsonify(flavors_list),200
    
    def getNetworkDetails():
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        data = request.json
        try:
        # List all servers and filter by the given server name
            network = creds_conn.network.networks()
            filtered_server = None
            name = data['resourcename']

            for network in network:
                if network.name == name:
                    filtered_server = network
                    break  # Stop once we find the matching server

            # If server is found, return its details
            if filtered_server:
                network_details = {
                    "id": filtered_server.id,
                    "name": filtered_server.name,
                    "status": filtered_server.status,
                    "is_admin_state_up": filtered_server.is_admin_state_up,
                    "subnets": filtered_server.subnet_ids,
                    "availability_zones": filtered_server.availability_zones, 
                    "port_security_enabled": filtered_server.is_port_security_enabled, 
                    "tags": filtered_server.tags, 
                    "created_at": filtered_server.created_at, 
                    "updated_at": filtered_server.updated_at, 
                    "revision_number": filtered_server.revision_number, 
                    "project_id": filtered_server.project_id, 
                    "tenant_id": filtered_server.tenant_id, 
                }
                return jsonify(network_details), 200
            else:
                return jsonify({"error": "Server not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500 
    
    def getNetworkNameList():
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        network_list = []
        for network in creds_conn.network.networks():
            network_list.append(network.name)

        return jsonify(network_list),200

    # Find Utilities
    def findServer(server_name):
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        find_server = creds_conn.compute.find_server(server_name)
        return find_server

    def findImage(image_id):
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        find_image = creds_conn.image.find_image(image_id)
        return find_image

    def findNetwork(network_name):
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        find_network = creds_conn.network.find_network(network_name)
        return find_network

    def findFlavor(flavor_type):
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        find_flavor = creds_conn.compute.find_flavor(flavor_type)
        return find_flavor

    def findSecurityGroup():
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        find_security_group =  creds_conn.network.find_security_group()
        return find_security_group

    

    # Create Utilities
    def createServer(instname,imageid,flavorid,network,securitygroup):
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        server_details = creds_conn.compute.create_server(
            name = instname,
            image_id=imageid,
            flavor_id=flavorid,
            networks=network,
            security_group=securitygroup
        )

        return server_details
    
    def createIP(public_network_id):
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        create_ip = creds_conn.network.create_ip(floating_network_id=public_network_id)
        return create_ip
    

    def deleteableInstanceList():
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        servers = creds_conn.compute.servers()
        deleteable_server_list = []
        for server in servers:
            if server.name not in ["backend2", "world1","openstackmini"]:
                print(server.name)
                deleteable_server_list.append(server.name)

        return deleteable_server_list


    # Delete Utilities 
    def deleteServer(servername):
        creds_conn = connection.Connection(cloud="CIS220074_IU")
        delete_server = creds_conn.compute.delete_server(server=servername)
        return delete_server
    
    def deleteFloatingIp(floatingip):
        creds_conn = connection.Connection(cloud="CIS220074_IU")

        if request.json:
            data = request.json
            floating_ip = data["floating_ip"]
        else:
            floating_ip = floatingip

        delete_floating_ip = creds_conn.network.delete_ip(floating_ip=floating_ip)
        return delete_floating_ip
    
    