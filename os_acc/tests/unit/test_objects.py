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

from oslo_versionedobjects import base as ovo_base
from oslo_versionedobjects import fixture

from os_acc import objects
from os_acc.tests.unit import base


object_data = {}


class TestObjectVersions(base.TestCase):
    def setUp(self):
        super(TestObjectVersions, self).setUp()

        objects.register_all()

    def test_versions(self):
        checker = fixture.ObjectVersionChecker(
            ovo_base.VersionedObjectRegistry.obj_classes())

        expected, actual = checker.test_hashes(object_data)
        self.assertEqual(expected, actual,
                         'Some objects have changed; please make sure the '
                         'versions have been bumped, and then update their '
                         'hashes here.')
