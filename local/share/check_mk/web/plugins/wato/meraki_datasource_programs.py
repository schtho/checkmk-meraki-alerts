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
)

from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)

from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourceProgramsHardware


def _valuespec_special_agents_meraki():
    return Dictionary(
        title=_("Cisco Meraki via REST API"),
        help=_(
            "This rule selects the Cisco Meraki REST API to collect data "
            "instead of the slow SNMP"),
        elements=[
            ('org_id', TextAscii(
                title=_('Organization ID'),
                allow_empty=False,
            )),
            ('api_key', TextAscii(
                title=_("API Key"),
                allow_empty=False,
            )),
            ("filter_tags",
                ListOfStrings(
                    title=_("Filter by Tags (Optional)"),
                    orientation="horizontal",
                    help=_("Filter Meraki Networks by Tags "
                           "Otherwise get all Meraki Networks "),
                    allow_empty=True,
                ),
            ),
            ("tags_filter_type",
                DropdownChoice(
                    title=_("Tags Filter Type"),
                    choices=[
                        (True, _("With Any Tags")),
                        (False, _("With All Tags")),
                    ],
                    default_value=True
                )),

        ],
        optional_keys=False,
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsHardware,
        name="special_agents:meraki",
        valuespec=_valuespec_special_agents_meraki,
    ))
