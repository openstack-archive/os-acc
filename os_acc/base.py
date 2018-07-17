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
import abc
from oslo_config import cfg
import six


CONF = cfg.CONF


@six.add_metaclass(abc.ABCMeta)
class PluginBase(object):
    """Base class for all ACC plugins."""

    # Override to provide a tuple of oslo_config.Opt instances for
    # the plugin config parameters
    CONFIG_OPTS = ()

    def __init__(self, config):
        """
        Initialize the plugin object with the provided config

        :param config: `oslo_config.ConfigOpts.GroupAttr` instance:
        """
        self.config = config

    @abc.abstractmethod
    def get_config(self, acc, instance=None, inst_type=None):
        """
        Generate config of specified accelerator.

        :param instance: Instance information dict.
        :param inst_type: Flavor information dict.
        :param acc: Accelerator information
        :return: Different LibvirtConfig. For example,
        `nova.virt.libvirt.config.LibvirtConfigGuestHostdevPCI` object.
        """

    @abc.abstractmethod
    def attach(self, acc, guest=None, host=None, instance=None,
               inst_type=None):
        """
        Given required parameters, perform operations to attach the ACC
        properly.

        :param acc: Accelerator information
        :param guest: `nova.virt.libvirt.guest.Guest` object.
        :param host: `nova.virt.libvirt.guest.Host` object.
        :param instance: Instance information dict.
        :param inst_type: Flavor information dict.
        :return:
        """

    @abc.abstractmethod
    def detach(self, acc, guest=None, host=None, instance=None,
               inst_type=None):
        """
        Given required parameters, perform operations to detach the ACC
        properly.

        :param acc: Accelerator information
        :param guest: `nova.virt.libvirt.guest.Guest` object.
        :param host: `nova.virt.libvirt.guest.Host` object.
        :param instance: Instance information dict.
        :param inst_type: Flavor information dict.
        :return:
        """

    @classmethod
    def load(cls, plugin_name):
        """
        Load a plugin, registering its configuration options

        :param plugin_name: the name of the plugin extension

        :returns: an initialized instance of the class
        """
        cfg_group_name = "os_acc_" + plugin_name
        cfg_opts = getattr(cls, "CONFIG_OPTS")
        cfg_vals = None
        if cfg_opts and len(cfg_opts) > 0:
            cfg_group = cfg.OptGroup(
                cfg_group_name,
                "os-acc plugin %s options" % plugin_name)
            CONF.register_opts(cfg_opts, group=cfg_group)

            cfg_vals = getattr(CONF, cfg_group_name)
        return cls(cfg_vals)
