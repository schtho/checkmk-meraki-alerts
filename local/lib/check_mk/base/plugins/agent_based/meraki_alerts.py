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

from .agent_based_api.v1 import *


def discover_meraki_alerts(section):
    yield Service()


def check_meraki_alerts(params, section):

    for alert_categoryType, alert_deviceType, alert_type, alert_title, alert_severity, alert_scope in section:

        err_text = f"[{alert_scope}]: {alert_title}"
        err_details = f"[{alert_scope}]: {alert_title} [{alert_type}][{alert_categoryType}]"
        if alert_severity == "warning":
            yield Result(state=State.WARN, summary=err_text, details=err_details)
        elif alert_severity == "critical":
            yield Result(state=State.CRIT, summary=err_text, details=err_details)
        else:
            yield Result(state=State.OK, summary="OK", details=err_details)

    if len(section) == 0:
        yield Result(state=State.OK, summary="OK")


register.check_plugin(
    name = "meraki_alerts",
    service_name = "Meraki Alerts",
    sections=["meraki_alerts"],
    discovery_function = discover_meraki_alerts,
    check_function = check_meraki_alerts,
    check_default_parameters={}, # not implemented yet
    check_ruleset_name="meraki_alerts_ruleset",
)