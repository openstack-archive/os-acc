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
        os_acc.initialize()

    @mock.patch.object(os_acc.pci.PciAccelerator, 'attach')
    def test_attach_pci_device(self, mock_attach):
        fake_acc = {"instance_uuid": "", "type": "pci",
                    "name": "NVIDIA Corporation GP100GL",
                    "pcie_address": "0000:81:00.0"}
        fake_instance = {}
        fake_inst_type = {}
        fake_guest = ""
        fake_host = ""

        os_acc.attach(fake_acc, fake_guest, fake_host, fake_instance,
                      fake_inst_type)
        mock_attach.assert_called_once_with(fake_acc, fake_guest,
                                            fake_host, fake_instance,
                                            fake_inst_type)

    @mock.patch.object(pci.PciAccelerator, 'detach')
    def test_detach_pci_device(self, mock_detach):
        fake_acc = {"instance_uuid": "", "type": "pci",
                    "name": "NVIDIA Corporation GP100GL",
                    "pcie_address": "0000:81:00.0"}
        fake_instance = {}
        fake_inst_type = {}
        fake_guest = ""
        fake_host = ""

        os_acc.detach(fake_acc, fake_guest, fake_host, fake_instance,
                      fake_inst_type)
        mock_detach.assert_called_once_with(fake_acc, fake_guest,
                                            fake_host, fake_instance,
                                            fake_inst_type)
