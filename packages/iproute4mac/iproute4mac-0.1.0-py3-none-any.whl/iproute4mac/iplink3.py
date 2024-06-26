import json
import os
import re
import subprocess
import sys

from iproute4mac.utils import *

import _ctypes


''' Options '''
option = {}


class NoIndent(object):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        reps = (repr(v) for v in self.value)
        return '[ ' + ','.join(reps) + ' ]'

def ref(obj_id):
    return _ctypes.PyObj_FromPtr(obj_id)

def json_unindent_list(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = json_unindent_list(v)
    elif isinstance(obj, list):
        if all(isinstance(x, str) for x in obj):
            return NoIndent(obj)
        for i, l in enumerate(obj):
            obj[i] = json_unindent_list(l)
    return obj

class IpRouteJSON(json.JSONEncoder):
    FORMAT_SPEC = "@@{}@@"
    regex = re.compile(FORMAT_SPEC.format(r"(\d+)"))

    def default(self, obj):
        if isinstance(obj, NoIndent):
            return self.FORMAT_SPEC.format(id(obj))
        return super(IpRouteJSON, self).default(obj)

    def encode(self, obj):
        obj = json_unindent_list(obj)
        format_spec = self.FORMAT_SPEC
        json_repr = super(IpRouteJSON, self).encode(obj)
        for match in self.regex.finditer(json_repr):
            id = int(match.group(1))
            json_repr = json_repr.replace('"{}"'.format(format_spec.format(id)), repr(ref(id)))
        json_repr = json_repr.replace("'", '"')
        json_repr = re.sub(r"\[\n\s+{", r"[ {", json_repr)
        json_repr = re.sub(r"},\n\s+{", r"},{", json_repr)
        json_repr = re.sub(r"}\n\s*\]", r"} ]", json_repr)
        return json_repr

def iproute_json(data):
    if option['pretty']:
        return json.dumps(data, cls=IpRouteJSON, indent=4)
    else:
        return json.dumps(data, separators=(",", ":"))
    

def parse_ifconfig(res, address=False):
    links = []
    count = 1

    for r in res.split("\n"):
        if re.match(r"^\w+:", r):
            if count > 1:
                links.append(link)
            (ifname, flags, mtu, ifindex) = re.findall(r"^(\w+): flags=\d+<(.*)> mtu (\d+) index (\d+)", r)[0]
            flags = flags.split(",") if flags != "" else []
            link = {
                "ifindex": int(ifindex),
                "ifname": ifname,
                "flags": flags,
                "mtu": int(mtu),
                "operstate": "UNKNOWN",
                "link_type": "unknown"
            }
            if "LOOPBACK" in flags:
                link["link_type"] = "loopback"
                link["address"] = "00:00:00:00:00:00"
                link["broadcast"] = "00:00:00:00:00:00"
            elif "POINTOPOINT" in flags:
                link["link_type"] = "none"
            count = count + 1
        else:
            if re.match(r"^\s+ether ", r):
                link["link_type"] = "ether"
                link["address"] = re.findall(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", r)[0]
                link["broadcast"] = "ff:ff:ff:ff:ff:ff"
            elif (address and
                  re.match(r"^\s+inet ", r) and
                  preferred_family != AF_INET6):
                (local, netmask) = re.findall(r"inet (\d+\.\d+\.\d+\.\d+).* netmask (0x[0-9a-f]+)", r)[0]
                addr = { "family": "inet", "local": local }
                if re.match(r"^.*-->", r):
                    addr["address"] = re.findall(r"--> (\d+\.\d+\.\d+\.\d+)", r)[0]
                addr["prefixlen"] = netmask_to_length(netmask)
                if re.match(r"^.*broadcast", r):
                    addr["broadcast"] = re.findall(r"broadcast (\d+\.\d+\.\d+\.\d+)", r)[0]
                link["addr_info"] = link.get("addr_info", []) + [addr]
            elif (address and
                  re.match(r"^\s+inet6 ", r) and
                  preferred_family != AF_INET):
                (local, prefixlen) = re.findall(r"inet6 ([0-9a-f:]*::[0-9a-f:]+)%*\w* prefixlen (\d+)", r)[0]
                link["addr_info"] = link.get("addr_info", []) + [{
                  "family": "inet6",
                  "local": local,
                  "prefixlen": int(prefixlen)
                }]
            elif re.match(r"^\s+status: ", r):
                link["operstate"] = oper_states[re.findall(r"status: (\w+)", r)[0]]
            elif re.match(r"^\s+vlan: ", r):
                (vid, vlink) = re.findall(r"vlan: (\d+) parent interface: (<?\w+>?)", r)[0]
                link["link"] = vlink
                if option['show_details']:
                    link["linkinfo"] = {
                        "info_kind": "vlan",
                        "info_data": {
                            "protocol": "802.1Q",
                            "id": int(vid),
                            "flags": []
                        }
                    }
            elif re.match(r"^\s+member: ", r):
                dev = re.findall(r"member: (\w+)", r)[0]
                index = next((i for (i, l) in enumerate(links) if l["ifname"] == dev), None)
                links[index]["master"] = ifname

    if count > 1:
        links.append(link)

    return links

def do_iplink_list(argv=[]):
    cmd = subprocess.run(['ifconfig', '-v', '-a'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         encoding="utf-8")
    if cmd.returncode == 0:
        links = parse_ifconfig(cmd.stdout, address=False)
        if option['json']:
            print(iproute_json(links))
        else:
            #print(iproure_text(links))
            print(cmd.stdout)
    else:
        print(cmd.stderr)

    return cmd.returncode


def do_iplink(argv=[], opts={}):
    global option
    option = opts

    if not argv:
        return iplink_list()

    cmd = argv.pop(0)
    if 'add'.startswith(cmd):
        return do_notimplemented()
    elif ('set'.startswith(cmd) or
          'change'.startswith(cmd)):
        return do_notimplemented()
    elif 'replace'.startswith(cmd):
        return do_notimplemented()
    elif 'delete'.startswith(cmd):
        return do_notimplemented()
    elif ('show'.startswith(cmd) or
          'lst'.startswith(cmd) or
          'list'.startswith(cmd)):
        return do_iplink_list(argv)
    elif 'xstats'.startswith(cmd):
        return do_notimplemented()
    elif 'afstats'.startswith(cmd):
        return do_notimplemented()
    elif 'property'.startswith(cmd):
        return do_notimplemented()
    elif 'help'.startswith(cmd):
        return do_notimplemented()

    stderr('Command "%s" is unknown, try "ip link help".' % cmd)
    exit(-1)
