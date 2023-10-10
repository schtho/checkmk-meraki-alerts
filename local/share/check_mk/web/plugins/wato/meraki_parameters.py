#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    TextAscii,
    Password,
    MonitoringState,
    Percentage,
    Tuple,
    Integer,
    Float
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersNetworking,
)

def _item_valuespec_foobar():
    return TextAscii(title=_("Sector name"))

# not implemented yet
def _parameter_valuespec_foobar():
    return Dictionary(
        elements=[
            ("error_rate", Tuple(
                title=_("Levels for port error rates"),
                elements=[
                    Percentage(title=_("Warning at"), default_value=0.010),
                    Percentage(title=_("Critical at"), default_value=0.100),
                ],
            )),
            ("port_aggr_state",
             MonitoringState(title=_("Operational state if port is aggregated"), default_value=1)),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="meraki_ruleset",
        group=RulespecGroupCheckParametersNetworking,
        match_type="dict",
        item_spec=_item_valuespec_foobar,
        parameter_valuespec=_parameter_valuespec_foobar,
        title=lambda: _("Cisco Meraki via API Settings"),
    ))
