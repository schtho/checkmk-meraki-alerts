# © Thomas Schmeiduch <https://github.com/schtho>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

import base64
from .agent_based_api.v1 import *
import json


def discover_meraki(section):
    for name, _status, _producttype, _model, _serial, _ip, _details, _sw_device_tags in section:
        yield Service(item=name)

def check_meraki(item, params, section):

    for name, status, producttype, model, serial, ip, details, sw_device_tags in section:
#        print(details)
        if item == name:

            # Get tags of Meraki device
            device_tags = convert_device_tags_string_to_list(sw_device_tags)

            # check if device is exluded from monitoring
            if "no-monitor" in device_tags:
                yield Result(state=State.OK, summary= f"Device is not monitored!")
                continue

            cmk_state = State.UNKNOWN
            if status == "offline":
                yield Result(state=State.CRIT, summary= f"Device is offline!")
                continue
            if status == "alerting":
                yield Result(state=State.WARN, summary= f"Device alerting!")
            if status == "dormant":
                yield Result(state=State.UNKNOWN, summary= f"Device dormant!")
                continue
            if status == "online":
                yield Result(state=State.OK, summary= f"[{model}][{ip}] Online")

            if producttype == "switch":
                # convert base64 to dict
                base64_bytes = details.encode('ascii')
                sw_ports_str = base64.b64decode(base64_bytes)
#                print(sw_ports_str)
                sw_ports_dict = json.loads(sw_ports_str)

                # get tags of switch with cmk:
                ports_tags_dict = convert_sw_device_tags_to_ports_dict(sw_device_tags)

                for port_dict in sw_ports_dict:
                    if "enabled" in port_dict and not port_dict["enabled"]:
                        # Port is deactivated
                        continue

                    # get tags of port
                    tag_no_cdp = False
                    tag_enforce = False
                    tag_no_monitor = False
#                    print(ports_tags_dict)
                    if port_dict['portId'] in ports_tags_dict:
                        lst = ports_tags_dict[port_dict['portId']]
                        if "no-cdp" in lst:
                            tag_no_cdp = True
                        if "enforce" in lst:
                            tag_enforce = True
                        if "no-monitor" in lst:
                            tag_no_monitor = True

                    # ignore Status on port
                    if tag_no_monitor:
                        continue

                    if "warnings" in port_dict:
                        if len(port_dict["warnings"]) != 0:
                            for elem in port_dict["warnings"]:
                                err = f"[Port {port_dict['portId']}]: {elem}"
                                yield Result(state=State.WARN, summary=err)

                    if "errors" in port_dict:
                        if len(port_dict["errors"]) != 0:
                            for elem in port_dict["errors"]:
                                err = f"[Port {port_dict['portId']}]: {elem}"
                                if elem == "Port disconnected":
                                    if tag_no_cdp is False and "cdp" in port_dict and "lldp" in port_dict:
                                        err += f" (to {port_dict['lldp']['systemName'] if 'systemName' in port_dict['lldp'] else port_dict['cdp']['address']} {port_dict['cdp']['portId']})"
                                        yield Result(state=State.CRIT, summary=err)
                                    if tag_enforce is False:
                                        continue
                                yield Result(state=State.CRIT, summary=err)

            return


def convert_device_tags_string_to_list(device_tags):
    if not device_tags:
        return []

    tags = device_tags.split(",")
    cmk_tags = [tag.removeprefix('cmk:') for tag in tags if tag.startswith('cmk:')]
    return cmk_tags


def convert_sw_device_tags_to_ports_dict(sw_device_tags):
    if not sw_device_tags:
        return {}

    cmk_tags = convert_device_tags_string_to_list(sw_device_tags)
    ports_tags_dict = {}

    for cmk_tag in cmk_tags:
        if ":" not in cmk_tag:
            continue
        tag_details = cmk_tag.split(":")
        port_no = tag_details[0]
        port_tag = tag_details[1]

        if port_no not in ports_tags_dict:
            ports_tags_dict[port_no] = []
        ports_tags_dict[port_no].append(port_tag)
    
    return ports_tags_dict


register.check_plugin(
    name = "meraki",
    service_name = "Meraki %s",
    sections=["meraki"],
    discovery_function = discover_meraki,
    check_function = check_meraki,
    check_default_parameters={"error_rate": (0.010, 0.100), "port_aggr_state": 1}, # not implemented yet
    check_ruleset_name="meraki_ruleset",
)
