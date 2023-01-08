import os
import subprocess

DIR_PATH = os.path.abspath(os.path.dirname(__file__))


def add_ip_to_firewall(ip, network_template):
    return subprocess.call(
        [
            "bash",
            os.path.join(DIR_PATH, "shell_scripts/temp.sh"),
            str(ip),
            str(network_template),
        ]
    )
