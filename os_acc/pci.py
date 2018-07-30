# Copyright 2018 Beijing Lenovo Software Ltd.
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

from os_acc import base


class PciAccelerator(base.PluginBase):

    def get_config(self, acc, instance=None, inst_type=None):
        pcie_addr = acc["address"]
        domain, bus, slot, func = self._get_pci_address_fields(pcie_addr)
        from nova.virt.libvirt.config import LibvirtConfigGuestHostdevPCI
        conf = LibvirtConfigGuestHostdevPCI()
        conf.domain = domain
        conf.bus = bus
        conf.slot = slot
        conf.function = func
        return conf

    def attach(self, acc, guest=None, host=None, instance=None,
               inst_type=None):
        conf = self.get_config(instance, inst_type, acc)
        state = guest.get_power_state(host)
        from nova.compute import power_state
        live = state in (power_state.RUNNING, power_state.PAUSED)
        guest.attach_device(conf, persistent=True, live=live)

    def detach(self, acc, guest=None, host=None, instance=None,
               inst_type=None):
        conf = self.get_config(instance, inst_type, acc)
        state = guest.get_power_state(host)
        from nova.compute import power_state
        live = state in (power_state.RUNNING, power_state.PAUSED)
        guest.detach_device(conf, persistent=True, live=live)

    def _get_pci_address_fields(self, pci_addr):
        """Parse a fully-specified PCI device address.

        :param pci_addr: A string of the form
        "<domain>:<bus>:<slot>.<function>".
        :return: A 4-tuple of strings
        ("<domain>", "<bus>", "<slot>", "<function>")
        """
        dbs, sep, func = pci_addr.partition('.')
        domain, bus, slot = dbs.split(':')
        return domain, bus, slot, func
