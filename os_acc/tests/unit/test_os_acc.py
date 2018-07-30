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
from oslo_config import cfg
from stevedore import extension

import os_acc
from os_acc import base as plugin_base
from os_acc import exception
from os_acc.tests.unit import base


class DemoPlugin(plugin_base.PluginBase):

    CONFIG_OPTS = (
        cfg.BoolOpt("make_it_work",
                    default=False,
                    help="Make everything work correctly by setting this"),
        cfg.IntOpt("sleep_time",
                   default=0,
                   help="How long to artifically sleep")
    )

    def get_config(self, acc, instance=None, inst_type=None):
        pass

    def attach(self, acc, guest=None, host=None, instance=None,
               inst_type=None):
        pass

    def detach(self, acc, guest=None, host=None, instance=None,
               inst_type=None):
        pass


class DemoPluginNoConfig(plugin_base.PluginBase):

    def get_config(self, acc, instance=None, inst_type=None):
        pass

    def attach(self, acc, guest=None, host=None, instance=None,
               inst_type=None):
        pass

    def detach(self, acc, guest=None, host=None, instance=None,
               inst_type=None):
        pass


class TestOSACC(base.TestCase):

    def setUp(self):
        super(TestOSACC, self).setUp()
        os_acc._EXT_MANAGER = None

    @mock.patch('stevedore.extension.ExtensionManager')
    def test_initialize(self, mock_EM):
        self.assertIsNone(os_acc._EXT_MANAGER)
        # Note: the duplicate call for initialize is to validate
        # that the extension manager is only initialized once
        os_acc.initialize()
        os_acc.initialize()
        mock_EM.assert_called_once_with(
            invoke_on_load=False, namespace='os_acc')
        self.assertIsNotNone(os_acc._EXT_MANAGER)

    def test_load_plugin(self):
        obj = DemoPlugin.load("demo")
        self.assertTrue(hasattr(cfg.CONF, "os_acc_demo"))
        self.assertTrue(hasattr(cfg.CONF.os_acc_demo, "make_it_work"))
        self.assertTrue(hasattr(cfg.CONF.os_acc_demo, "sleep_time"))
        self.assertEqual(cfg.CONF.os_acc_demo.make_it_work, False)
        self.assertEqual(cfg.CONF.os_acc_demo.sleep_time, 0)

        self.assertEqual(obj.config, cfg.CONF.os_acc_demo)

    def test_load_plugin_no_config(self):
        obj = DemoPluginNoConfig.load("demonocfg")
        self.assertFalse(hasattr(cfg.CONF, "os_acc_demonocfg"))

        self.assertIsNone(obj.config)

    def test_attach_not_initialized(self):
        self.assertRaises(
            exception.LibraryNotInitialized,
            os_acc.attach, None, None, None, None, None)

    def test_detach_not_initialized(self):
        self.assertRaises(
            exception.LibraryNotInitialized,
            os_acc.detach, None, None, None, None, None)

    @mock.patch.object(DemoPlugin, "attach")
    def test_attach(self, mock_attach):
        plg = extension.Extension(name="demo",
                                  entry_point="os-acc",
                                  plugin=DemoPlugin,
                                  obj=None)
        with mock.patch('stevedore.extension.ExtensionManager.names',
                        return_value=['foobar']),\
                mock.patch('stevedore.extension.ExtensionManager.__getitem__',
                           return_value=plg):
            os_acc.initialize()
            fake_acc = {"instance_uuid": "", "interface_type": "demo",
                        "name": "NVIDIA Corporation GP100GL",
                        "address": "0000:81:00.0"}
            fake_instance = {}
            fake_inst_type = {}
            fake_guest = ""
            fake_host = ""
            os_acc.attach(fake_acc, fake_guest, fake_host, fake_instance,
                          fake_inst_type)
            mock_attach.assert_called_once_with(fake_acc, fake_guest,
                                                fake_host, fake_instance,
                                                fake_inst_type)

    @mock.patch.object(DemoPlugin, "get_config")
    def test_get_config(self, mock_get_config):
        plg = extension.Extension(name="demo",
                                  entry_point="os-acc",
                                  plugin=DemoPlugin,
                                  obj=None)
        with mock.patch('stevedore.extension.ExtensionManager.names',
                        return_value=['foobar']),\
                mock.patch('stevedore.extension.ExtensionManager.__getitem__',
                           return_value=plg):
            os_acc.initialize()
            fake_acc = {"instance_uuid": "", "interface_type": "demo",
                        "name": "NVIDIA Corporation GP100GL",
                        "address": "0000:81:00.0"}
            fake_instance = {}
            fake_inst_type = {}
            os_acc.get_config(fake_acc, fake_instance, fake_inst_type)
            mock_get_config.assert_called_once_with(fake_acc, fake_instance,
                                                    fake_inst_type)

    @mock.patch.object(DemoPlugin, "detach")
    def test_detach(self, mock_detach):
        plg = extension.Extension(name="demo",
                                  entry_point="os-acc",
                                  plugin=DemoPlugin,
                                  obj=None)
        with mock.patch('stevedore.extension.ExtensionManager.names',
                        return_value=['foobar']),\
                mock.patch('stevedore.extension.ExtensionManager.__getitem__',
                           return_value=plg):
            os_acc.initialize()
            fake_acc = {"instance_uuid": "", "interface_type": "demo",
                        "name": "NVIDIA Corporation GP100GL",
                        "address": "0000:81:00.0"}
            fake_instance = {}
            fake_inst_type = {}
            fake_guest = ""
            fake_host = ""
            os_acc.detach(fake_acc, fake_guest, fake_host, fake_instance,
                          fake_inst_type)
            mock_detach.assert_called_once_with(fake_acc, fake_guest,
                                                fake_host, fake_instance,
                                                fake_inst_type)
