# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command-line interface to the OpenStack Craton API V1."""
from cratonclient.shell.v1 import cells_shell
from cratonclient.shell.v1 import hosts_shell
from cratonclient.shell.v1 import regions_shell


COMMAND_MODULES = [
    # TODO(cmspence): project_shell, cell_shell, device_shell, user_shell, etc.
    regions_shell,
    hosts_shell,
    cells_shell,
]
