import requests as r
import json
import ipaddress

# Init variables
print('Please enter the Router IP')
ROUTER_IP = input()
print('Please enter the Interal Client IP (aka server)')
INTERNAL_CLIENT = input()
print('Please input the PORT')
PORT = input()
print('Please enter a name for the rule')
NAME = input()
print('Please enter the SID (cookie)')
SID = input()
print('Please enter the _sessionTOKEN')
SESSION_TOKEN = input()

# Retrieves the first and last host available in a network from a CIDR notated network
def cidr_to_ip_range(cidr: str) -> list[str]:
    network = ipaddress.ip_network(cidr)
    return [str(list(network.hosts())[0]), str(list(network.hosts())[-1])]

# Retrieve IPv4 Ranges from CloudFlare
def retrieve_ip_list():
    header = {"Content-Type": "application/json"}
    response = r.get("https://api.cloudflare.com/client/v4/ips", headers=header)
    dictionary = json.loads(response.text)
    return dictionary['result']['ipv4_cidrs']

# Sends the request for a new rule to the router
def create_new_rule(remote_host, remote_host_end, internal_client, port, session_token, sid, description, router_ip):
    payload = {
        "IF_ACTION": "Apply",
        "OBJ_FWPM_ID.Enable": "1",
        "OBJ_FWPM_ID._OBJ_InstID": "-1",
        "OBJ_FWPM_ID.Description": description,
        "OBJ_FWPM_ID.Protocol": "BOTH",
        "OBJ_FWPM_ID.RemoteHost": remote_host,
        "OBJ_FWPM_ID.RemoteHostEndRange": remote_host_end,
        "OBJ_FWPM_ID.InternalClient": internal_client,
        "OBJ_FWPM_ID.ExternalPort": port,
        "OBJ_FWPM_ID.ExternalPortEndRange": port,
        "OBJ_FWPM_ID.InternalPort": port,
        "_sessionTOKEN": session_token
    }
    headers = {
        "Cookie": f"_TESTCOOKIESUPPORT=1; SID={sid}"
    }
    post_request = r.post(f'http://{router_ip}/?_type=menuData&_tag=firewall_portforwarding_m.lua', data=payload, headers=headers)
    if (post_request.status_code == 200):
        return True
    return False

for ips in retrieve_ip_list():
    remote_host, remote_host_end = cidr_to_ip_range(ips)
    description = f"{NAME}_CF_{ips}"
    internal_client = INTERNAL_CLIENT
    port = PORT
    session_token = SESSION_TOKEN
    sid = SID
    router_ip = ROUTER_IP
    if (create_new_rule(remote_host, remote_host_end, internal_client, port, session_token, sid, description, router_ip)):
        print(f"OK - {ips} has been added correctly")
    else:
        print(f"ERROR - {ips} wasn't added")