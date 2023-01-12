import os
import subprocess
from networkuiapp.database import db


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


class Template:
    bandwidth_restriction_upload: int
    bandwidth_restriction_download: int
    dns_latency: int
    general_latency: int
    packet_loss: int

    def __init__(
        self,
        bandwidth_restriction_upload: int,
        bandwidth_restriction_download: int,
        dns_latency: int,
        general_latency: int,
        packet_loss: int,
    ) -> None:
        self.bandwidth_restriction_upload = bandwidth_restriction_upload
        self.bandwidth_restriction_download = bandwidth_restriction_download
        self.dns_latency = dns_latency
        self.general_latency = general_latency
        self.packet_loss = packet_loss


class Welcome10Value:
    pcs: list[str]
    template: Template
    name: str

    def __init__(self, pcs: list[str], template: Template, name: str) -> None:
        self.pcs = pcs
        self.template = template
        self.name = name


def make_json_endpoint(IPAddress, NetworkTemplate):
    network_templates = NetworkTemplate.query.all()

    for network_template in network_templates:
        print(
            [
                ip.ip_address
                for ip in IPAddress.query.filter(
                    IPAddress.network_template == network_template.id
                ).all()
            ]
        )

        print(network_template.__dict__.get("id"))


# example JSON
# {
#   "1": {
#     "pcs": [
#       "192.168.1.1",
#       "192.168.1.2",
#       "192.168.1.3"
#     ],
#     "template": {
#       "bandwidth_restriction_upload": "10",
#       "bandwidth_restriction_download": "15",
#       "dns_latency": "35",
#       "general_latency": "54",
#       "packet_loss": "100"
#     },
#     "name": "good network"
#   },
#   "2": {
#     "pcs": [
#       "192.168.1.1",
#       "192.168.1.2",
#       "192.168.1.3"
#     ],
#     "template": {
#       "bandwidth_restriction_upload": "10",
#       "bandwidth_restriction_download": "15",
#       "dns_latency": "35",
#       "general_latency": "54",
#       "packet_loss": "100"
#     },
#     "name": "Bad network"
#   }
# }
