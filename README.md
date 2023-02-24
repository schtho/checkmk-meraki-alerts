# Checkmk Plugin for Cisco Meraki Cloud Dashboard

This plugin provides a support for the monitoring of Meraki devices via the REST API.

## Usage Information

This Plugin works with Piggyback. You have to add additional Hosts in the form of `Meraki-{MERAKI_NET}`. For example, if you have the Meraki network `Home` the corresponding Host is called `Meraki-Home`. Checkmk piggybacks the data to that host.

## Documentation Agent

That plugin is a special agent. The ruleset is comparable to vSphere or other CMK rulesets.

The plugin provides several files:

First, define the special agent ruleset with the necessary parameters in wato. In addition to that, each CMK service can also follow specific rules of rule sets. For that, we also define a rule set for our meraki services:
```bash
OMD[site]:~$ nano ~/local/share/check_mk/web/plugins/wato/meraki_datasource_programs.py

# WATO Settings for Service
OMD[site]:~$ nano ~/local/share/check_mk/web/plugins/wato/meraki_parameters.py
```

Checkmk takes these parameters of wato and uses them to call the special agent. The parameters how to call the executable agent is defined in this file:

```bash
OMD[site]:~$ nano ~/local/share/check_mk/checks/agent_meraki
```

Checkmk calls the following script with the previously defined parameters for the "executable". That agent produces raw data which is analyzed in a latter step:

```bash
OMD[site]:~$ nano ~/local/share/check_mk/agents/special/agent_meraki
```

At the end, Checkmk analyzes and monitors the given services by the rules defined in this file:

```bash
OMD[site]:~$ nano ~/local/lib/check_mk/base/plugins/agent_based/meraki.py
```

## Documentation Usage

Create a new CMK Host, for example with the IP Address 127.0.0.1.  
Use as Monitoring Agent: `Configured API integrations, no Checkmk agent`

Look at `Other integrations` for `Cisco Meraki via REST API` and configure the rules.

## Usage Meraki
The plugin supports tags on Meraki switches. You can add them to the switch via Meraki Dashboard and can set ports of the switch:
- `cmk:PORTID:no-monitor`: Ignore errors and warnings on that port. For example: `cmk:12:no-monitor`: ignore errors on port 12.
- `cmk:PORTID:cdp`: Use CDP/LLDP data showing the connected device if port is disconnected.
- `cmk:PORTID:enforce`: Monitor offline state of a port.
- `cmk:no-monitor`: Ignore device

## Other Plugins for Help
To support your understanding of checkmk plugin programming, take a look at:
- https://github.com/Yogibaer75/Check_MK-Things/blob/master/check%20plugins%202.0/meraki/agents/special/agent_meraki
- https://github.com/Yogibaer75/Check_MK-Things/tree/master/check%20plugins%202.0/dell_idrac_redfish
- https://exchange.checkmk.com/p/f5cloud

## Releases MKP File

Releases are available: https://github.com/schtho/checkmk-meraki/releases

## Other Documentation

- https://docs.checkmk.com/latest/de/labels.html#agent_plugins
- https://git.onesystems.ch/Monitoring/check_mk/-/blob/be4bd9501c77e4c2fea066c2e65c6abbb872e8d6/cmk/gui/plugins/wato/datasource_programs.py
- https://docs.checkmk.com/latest/de/piggyback.html?lquery=piggyback#_die_technik_dahinter
- Command to debug on CLI: `cmk --debug -vII --plugins meraki --check Meraki-Dashboard`
- Command to print the output of the raw data agent: `cmk -d Meraki-Dashboard`
