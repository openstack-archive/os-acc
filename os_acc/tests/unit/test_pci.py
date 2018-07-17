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

import mock

import os_acc
from os_acc import pci
from os_acc.tests.unit import base


class TestPCI(base.TestCase):

    def setUp(self):
        super(TestPCI, self).setUp()

    @mock.patch.object(pci.PciAccelerator, 'attach')
    def attach_pci_device(self, mock_attach):
        os_acc.initialize(reset=True)
        fake_acc = {"instance_uuid": "", "type": "pci",
                    "name": "NVIDIA Corporation GP100GL",
                    "pcie_address": "0000:81:00.0"}

        class FakeGuest(object):
            def attach_device(self, conf, persistent, live):
                pass

            def detach_device(self, conf, persistent, live):
                pass

            def get_power_state(self, host):
                pass

        fake_instance = {}
        fake_inst_type = {}
        fake_guest = FakeGuest()
        fake_host = ""
        os_acc.attach(fake_acc, fake_guest, fake_host, fake_instance,
                      fake_inst_type)
        mock_attach.assert_called_once_with(fake_acc, fake_guest,
                                            fake_host, fake_instance,
                                            fake_inst_type)

    @mock.patch.object(pci.PciAccelerator, 'detach')
    def detach_pci_device(self, mock_detach):
        os_acc.initialize(reset=True)
        fake_acc = {"instance_uuid": "", "type": "pci",
                    "name": "NVIDIA Corporation GP100GL",
                    "pcie_address": "0000:81:00.0"}

        class FakeGuest(object):
            def attach_device(self, conf, persistent, live):
                pass

            def detach_device(self, conf, persistent, live):
                pass

            def get_power_state(self, host):
                pass

        fake_instance = {}
        fake_inst_type = {}
        fake_guest = FakeGuest()
        fake_host = ""
        os_acc.detach(fake_acc, fake_guest, fake_host, fake_instance,
                      fake_inst_type)
        mock_detach.assert_called_once_with(fake_acc, fake_guest,
                                            fake_host, fake_instance,
                                            fake_inst_type)
