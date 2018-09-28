# Copyright 2018 Intel, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import re

_RC_FPGA = "CUSTOM_ACCELERATOR_FPGA"
# Querystring-related constants
_QS_RESOURCES = 'resources'
_QS_REQUIRED = 'required'
_QS_TRAITS = 'trait'
_QS_MEMBER_OF = 'member_of'
_QS_CYBORG = 'cyborg'
_QS_KEY_PATTERN = re.compile(
        r"^(%s)([1-9][0-9]*)?$" % '|'.join(
            (_QS_RESOURCES, _QS_TRAITS, _QS_MEMBER_OF)))

_QS_INTEL_REGION_PREFIX = "CUSTOM_FPGA_INTEL_REGION_"
_QS_INTEL_FPGA_MODEL_PREFIX = "CUSTOM_FPGA_INTEL_"
_QS_FPGA_FUNCTION_PREFIX = "CUSTOM_FPGA_"
_QS_INTEL_FUNCTION_PREFIX = "CUSTOM_FPGA_INTEL_FUNCTION_"
_QS_INTEL_FPGA = "CUSTOM_FPGA_INTEL"
_QS_INTEL_FPGA_ARRIA_RPEFIX = "ARRIA"
_QS_FPGA_PROGRAMMABLE = "CUSTOM_PROGRAMMABLE"
_QS_INTEL_AFUID_PATTERN = re.compile(
    r"^(%s)([a-fA-F0-9]{32,32})$" % _QS_INTEL_FUNCTION_PREFIX)
_QS_INTEL_AFUNAME_PATTERN = re.compile(
    r"^(%s)(.{1,128})$" % _QS_INTEL_FUNCTION_PREFIX)
_QS_INTEL_REGIONID_PATTERN = re.compile(
    r"^(%s)([a-fA-F0-9]{32,32})$" % _QS_INTEL_REGION_PREFIX)
_QS_INTEL_FPGA_ARRIA_PATTERN = re.compile(
    r"^(%s)(%s[0-9]{2,2})$" %
    (_QS_INTEL_FPGA_MODEL_PREFIX, _QS_INTEL_FPGA_ARRIA_RPEFIX))

VONDER_MAP = {"intel": "0x8086"}


def _get_request_spec(body):
    request_spec = {}
    for key, values in body.items():
        match = _QS_KEY_PATTERN.match(key)
        if match:
            prefix, suffix = match.groups()
            g_value = request_spec.setdefault(suffix,
                 {_QS_RESOURCES: {_RC_FPGA: 0},
                  _QS_TRAITS: {_QS_REQUIRED: []},
                  _QS_MEMBER_OF: [], _QS_CYBORG: []})
            if prefix == _QS_RESOURCES:
                for v in values:
                    rname, _, rnum = v.partition("=")
                    if rname in g_value[prefix]:
                        g_value[prefix][rname] = rnum
            elif prefix == _QS_TRAITS:
                for v in values:
                    rname, _, rsetting = v.partition("=")
                    if rsetting == _QS_REQUIRED:
                        g_value[prefix][rsetting].append(rname)

    return request_spec


def gen_intel_filter_from_traits(trait, filters):
    filters["vendor"] = VONDER_MAP["intel"]
    if "CUSTOM_FPGA_INTEL" not in trait:
        return {}
    m = _QS_INTEL_AFUID_PATTERN.match(trait)
    if m:
        _, afu_id = m.groups()
        filters["afu_id"] = afu_id
    m = _QS_INTEL_AFUNAME_PATTERN.match(trait)
    if m:
        _, afu_name = m.groups()
        filters["afu_name"] = afu_name
    m = _QS_INTEL_REGIONID_PATTERN.match(trait)
    if m:
        _, region_id = m.groups()
        filters["region_id"] = region_id
    m = _QS_INTEL_FPGA_ARRIA_PATTERN.match(trait)
    if m:
        _, model = m.groups()
        filters["model"] = model.lower()
    return filters


def parser(specs):
    """Function to parse the nova input param to cyborg's acceptable params"""
    import pdb
    pdb.set_trace()
    specs = _get_request_spec(specs)
    for _, spec in specs.items():
        traits = spec[_QS_TRAITS][_QS_REQUIRED]
        resources = spec[_QS_RESOURCES]
        filters = {}
        for k in resources.keys():
            if k.count("_") < 2:
                    continue
            device_type = k.split("_")[-1]
            device_type = k.split("_")[-1]
            filters["device_type"] = device_type
        for trait in traits:
            vendor = trait.split("_")[2]
            if vendor == "INTEL":
                filters = gen_intel_filter_from_traits(trait, filters)
            else:
                # TODO(Xinran): add other type of devices.
                filters = filters["vendor"] = vendor
        return filters
