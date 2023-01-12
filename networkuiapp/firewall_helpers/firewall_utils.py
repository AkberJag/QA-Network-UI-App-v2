import os
import json
from networkuiapp import config
from time import sleep

DIR_PATH = os.path.abspath(os.path.dirname(__file__))


def add_ip_to_firewall(ip, network_template):
    # return subprocess.call(
    #     [
    #         "bash",
    #         os.path.join(DIR_PATH, "shell_scripts/temp.sh"),
    #         str(ip),
    #         str(network_template),
    #     ]
    # )
    print("firewall call")


def make_json_endpoint(IPAddress, NetworkTemplate):
    """Generates a json file with network template parametes and the pcs in it
    # ? I Think this methord needs to be an async fn
    """
    json_end = {}

    config.is_a_script_running = True
    sleep(10)

    for nt in NetworkTemplate.query.all():
        pcs_in_template = [
            ip.ip_address
            for ip in IPAddress.query.filter(IPAddress.network_template == nt.id).all()
        ]
        if pcs_in_template:
            json_end[nt.__dict__.get("id")] = {
                "name": nt.__dict__.get("network_template_name"),
                "template": {
                    "bandwidth_restriction_upload": nt.__dict__.get(
                        "bandwidth_restriction_upload"
                    ),
                    "bandwidth_restriction_download": nt.__dict__.get(
                        "bandwidth_restriction_download"
                    ),
                    "dns_latency": nt.__dict__.get("dns_latency"),
                    "general_latency": nt.__dict__.get("general_latency"),
                    "packet_loss": nt.__dict__.get("packet_loss"),
                },
                "pcs": pcs_in_template,
            }

    with open("example.json", "w") as jsonfile:
        jsonfile.write(json.dumps(json_end))

    config.is_a_script_running = False
