#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_versionedobjects import base as ovo_base


class VersionedObject(ovo_base.VersionedObject):

    OBJ_PROJECT_NAMESPACE = 'os_acc'


class VersionedObjectPrintableMixin(object):
    """Mix-in to implement __str__ method for a versioned object

    If a versioned object needs to be printable in a easy-reading format,
    inherit from this class.
    """

    def __str__(self):
        if callable(getattr(self, 'obj_to_primitive', None)):
            return str(self.obj_to_primitive())
        return super(VersionedObjectPrintableMixin, self).__str__()
