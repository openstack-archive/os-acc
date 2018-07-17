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

from os_acc.i18n import _


class ExceptionBase(Exception):
    """Base Exception

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.

    """
    msg_fmt = _("An unknown exception occurred.")

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if not message:
            try:
                message = self.msg_fmt % kwargs
            except Exception:
                # at least get the core message out if something happened
                message = self.msg_fmt

        self.message = message
        super(ExceptionBase, self).__init__(message)

    def format_message(self):
        return self.args[0]


class LibraryNotInitialized(ExceptionBase):
    msg_fmt = _("Before using the os_acc library, you need to call "
                "os_acc.initialize()")


class AttachException(ExceptionBase):
    msg_fmt = _("Failed to attach ACC %(acc)s. Got error: %(err)s")


class DetachException(ExceptionBase):
    msg_fmt = _("Failed to detach ACC %(acc)s. Got error: %(err)s")


class InternalError(ExceptionBase):
    msg_fmt = _("%(err)s")


class NoMatchingPlugin(ExceptionBase):
    msg_fmt = _("No ACC plugin was found with the name %(plugin_name)s")
