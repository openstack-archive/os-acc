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

from oslo_log import log as logging
from stevedore import extension

import os_acc.exception
from os_acc.i18n import _

_EXT_MANAGER = None
LOG = logging.getLogger(__name__)


def initialize(reset=False):
    global _EXT_MANAGER
    if reset or (_EXT_MANAGER is None):
        _EXT_MANAGER = extension.ExtensionManager(namespace='os_acc',
                                                  invoke_on_load=False)
        loaded_plugins = []
        for plugin_name in _EXT_MANAGER.names():
            cls = _EXT_MANAGER[plugin_name].plugin
            obj = cls.load(plugin_name)
            LOG.debug(("Loaded ACC plugin class '%(cls)s' "
                       "with name '%(plugin_name)s'"),
                      {'cls': cls, 'plugin_name': plugin_name})
            loaded_plugins.append(plugin_name)
            _EXT_MANAGER[plugin_name].obj = obj
        LOG.info("Loaded ACC plugins: %s", ", ".join(loaded_plugins))


def get_config(acc, instance=None, inst_type=None):

    if _EXT_MANAGER is None:
        raise os_acc.exception.LibraryNotInitialized()
    acc_type = acc['interface_type']
    if acc_type is None:
        raise os_acc.exception.InternalError(
            _("acc_type parameter must be present "
              "for this acc_type implementation"))
    try:
        plugin = _EXT_MANAGER[acc_type].obj
    except KeyError:
        raise os_acc.exception.NoMatchingPlugin(plugin_name=acc_type)
    conf = plugin.get_config(acc, instance, inst_type)
    return conf


def attach(acc, guest=None, host=None, instance=None, inst_type=None):
    if _EXT_MANAGER is None:
        raise os_acc.exception.LibraryNotInitialized()
    acc_type = acc['interface_type']
    if acc_type is None:
        raise os_acc.exception.InternalError(
            _("acc_type parameter must be present "
              "for this acc_type implementation"))
    try:
        plugin = _EXT_MANAGER[acc_type].obj
    except KeyError:
        raise os_acc.exception.NoMatchingPlugin(plugin_name=acc_type)
    try:
        LOG.debug("Attach acc %s", acc)
        plugin.attach(acc, guest, host, instance, inst_type)
        LOG.info("Successfully Attached acc %s", acc)
    except Exception as err:
        LOG.error("Failed to attach acc %(acc)s",
                  {"acc": acc}, exc_info=True)
        raise os_acc.exception.AttachException(acc=acc, err=err)


def detach(acc, guest=None, host=None, instance=None, inst_type=None):

    if _EXT_MANAGER is None:
        raise os_acc.exception.LibraryNotInitialized()
    acc_type = acc['interface_type']
    if acc_type is None:
        raise os_acc.exception.InternalError(
            _("acc_type parameter must be present "
              "for this acc_type implementation"))
    try:
        plugin = _EXT_MANAGER[acc_type].obj
    except KeyError:
        raise os_acc.exception.NoMatchingPlugin(plugin_name=acc_type)

    try:
        LOG.debug("Detaching acc %s", acc)
        plugin.detach(acc, guest, host, instance, inst_type)
        LOG.info("Successfully detached acc %s", acc)
    except Exception as err:
        LOG.error("Failed to unplug acc %(acc)s",
                  {"acc": acc}, exc_info=True)
        raise os_acc.exception.DetachException(acc=acc, err=err)
