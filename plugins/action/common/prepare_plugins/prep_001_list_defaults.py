# Copyright (c) 2024 Cisco Systems, Inc. and its affiliates
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT


from ....plugin_utils.helper_functions import data_model_key_check


def update_nested_dict(nested_dict, keys, new_value):
    if len(keys) == 1:
        nested_dict[keys[0]] = new_value
    else:
        key = keys[0]
        if key in nested_dict:
            update_nested_dict(nested_dict[key], keys[1:], new_value)


class PreparePlugin:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.keys = []

    def set_list_default(self, parent_keys, target_key):
        keys = parent_keys + [target_key]
        dm_check = data_model_key_check(self.model_data, keys)
        if target_key in dm_check['keys_not_found'] or \
           target_key in dm_check['keys_no_data']:
            update_nested_dict(self.model_data, keys, [])

    # The prepare method is used to default each list or nested list
    # in the model data to an empty list if the key for the list does
    # not exist or data under they key does not exist.
    #
    # This is to ensure that the model data is consistent and can be
    # used by other plugins without having to check if the key exists.
    def prepare(self):
        self.model_data = self.kwargs['results']['model_extended']

        # --------------------------------------------------------------------
        # Fabric Global List Defaults
        # --------------------------------------------------------------------

        # Check vxlan.global list elements
        parent_keys = ['vxlan', 'global']
        target_key = 'dns_servers'
        self.set_list_default(parent_keys, target_key)

        # keys = ['vxlan', 'global', 'ntp_servers']
        parent_keys = ['vxlan', 'global']
        target_key = 'ntp_servers'
        self.set_list_default(parent_keys, target_key)

        # --------------------------------------------------------------------
        # Fabric Topology List Defaults
        # --------------------------------------------------------------------

        # Check vxlan.topology list elements
        parent_keys = ['vxlan', 'topology']
        dm_check = data_model_key_check(self.model_data, parent_keys)
        if 'topology' in dm_check['keys_no_data']:
            self.model_data['vxlan']['topology'] = {'edge_connections': []}
            self.model_data['vxlan']['topology'] = {'fabric_links': []}
            self.model_data['vxlan']['topology'] = {'switches': []}
            self.model_data['vxlan']['topology'] = {'vpc_peers': []}

        # Check vxlan.topology.fabric_links list element
        target_key = 'fabric_links'
        self.set_list_default(parent_keys, target_key)

        # Check vxlan.topology.edge_connections list element
        target_key = 'edge_connections'
        self.set_list_default(parent_keys, target_key)

        # Check vxlan.topology.switches list element
        target_key = 'switches'
        self.set_list_default(parent_keys, target_key)

        # Check vxlan.topology.vpc_peers list element
        target_key = 'vpc_peers'
        self.set_list_default(parent_keys, target_key)

        # --------------------------------------------------------------------
        # Fabric Topology Switches Freeforms List Defaults
        # --------------------------------------------------------------------

        # Check vxlan.topology.switches[index].freeforms list elements
        list_index = 0
        for switch in self.model_data['vxlan']['topology']['switches']:
            dm_check = data_model_key_check(switch, ['freeforms'])
            if 'freeforms' in dm_check['keys_not_found'] or \
               'freeforms' in dm_check['keys_no_data']:
                self.model_data['vxlan']['topology']['switches'][list_index]['freeforms'] = []

            list_index += 1

        # --------------------------------------------------------------------
        # Fabric Topology Switches Interfaces List Defaults
        # --------------------------------------------------------------------

        # Check vxlan.topology.switches[index].interfaces list elements
        list_index = 0
        for switch in self.model_data['vxlan']['topology']['switches']:
            dm_check = data_model_key_check(switch, ['interfaces'])
            if 'interfaces' in dm_check['keys_not_found'] or 'interfaces' in dm_check['keys_no_data']:
                self.model_data['vxlan']['topology']['switches'][list_index]['interfaces'] = []

            list_index += 1

        # --------------------------------------------------------------------
        # Fabric Overlay List Defaults
        # --------------------------------------------------------------------

        # Check vxlan.overlay_services list elements
        parent_keys = ['vxlan', 'overlay_services']
        dm_check = data_model_key_check(self.model_data, parent_keys)
        if 'overlay_services' in dm_check['keys_not_found'] or 'overlay_services' in dm_check['keys_no_data']:
            self.model_data['vxlan']['overlay_services'] = {'vrfs': []}
            self.model_data['vxlan']['overlay_services'] = {'vrf_attach_groups': []}
            self.model_data['vxlan']['overlay_services'] = {'networks': []}
            self.model_data['vxlan']['overlay_services'] = {'network_attach_groups': []}

        # Check vxlan.overlay_services.vrfs list element
        target_key = 'vrfs'
        self.set_list_default(parent_keys, target_key)

        # Check vxlan.overlay_services.vrf_attach_groups list element
        target_key = 'vrf_attach_groups'
        self.set_list_default(parent_keys, target_key)

        # Check vxlan.overlay_services.vrf_attach_groups[index].switches list elements
        list_index = 0
        for group in self.model_data['vxlan']['overlay_services']['vrf_attach_groups']:
            dm_check = data_model_key_check(group, ['switches'])
            if 'switches' in dm_check['keys_not_found'] or \
               'switches' in dm_check['keys_no_data']:
                self.model_data['vxlan']['overlay_services']['vrf_attach_groups'][list_index]['switches'] = []

            list_index += 1

        # Check vxlan.overlay_services.networks list element
        target_key = 'networks'
        self.set_list_default(parent_keys, target_key)

        # Check vxlan.overlay_services.network_attach_groups list element
        target_key = 'network_attach_groups'
        self.set_list_default(parent_keys, target_key)

        # Check vxlan.overlay_services.network_attach_groups[index].switches list elements
        list_index = 0
        for group in self.model_data['vxlan']['overlay_services']['network_attach_groups']:
            dm_check = data_model_key_check(group, ['switches'])
            if 'switches' in dm_check['keys_not_found'] or \
               'switches' in dm_check['keys_no_data']:
                self.model_data['vxlan']['overlay_services']['network_attach_groups'][list_index]['switches'] = []

            list_index += 1

        # --------------------------------------------------------------------
        # Fabric Policy List Defaults
        # --------------------------------------------------------------------

        # Check vxlan.policy list elements
        parent_keys = ['vxlan', 'policy']
        dm_check = data_model_key_check(self.model_data, parent_keys)
        if 'policy' in dm_check['keys_not_found'] or 'policy' in dm_check['keys_no_data']:
            self.model_data['vxlan']['policy'] = {}
            self.model_data['vxlan']['policy'].update({'policies': []})
            self.model_data['vxlan']['policy'].update({'groups': []})
            self.model_data['vxlan']['policy'].update({'switches': []})

        parent_keys = ['vxlan', 'policy', 'policies']
        dm_check = data_model_key_check(self.model_data, parent_keys)
        if 'policies' in dm_check['keys_not_found'] or 'policies' in dm_check['keys_no_data']:
            self.model_data['vxlan']['policy']['policies'] = []

        parent_keys = ['vxlan', 'policy', 'groups']
        dm_check = data_model_key_check(self.model_data, parent_keys)
        if 'groups' in dm_check['keys_not_found'] or 'groups' in dm_check['keys_no_data']:
            self.model_data['vxlan']['policy']['groups'] = []

        parent_keys = ['vxlan', 'policy', 'switches']
        dm_check = data_model_key_check(self.model_data, parent_keys)
        if 'switches' in dm_check['keys_not_found'] or 'switches' in dm_check['keys_no_data']:
            self.model_data['vxlan']['policy']['switches'] = []

        self.kwargs['results']['model_extended'] = self.model_data
        return self.kwargs['results']
