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
"""Hosts resource and resource shell wrapper."""
from __future__ import print_function

from cratonclient.common import cliutils
from cratonclient import exceptions as exc

DEFAULT_DEVICE_FIELDS = [
    'id',
    'name',
    'device_type',
    'ip_address',
    'cloud_id',
    'region_id',
    'cell_id',
]


DEVICE_FIELDS = DEFAULT_DEVICE_FIELDS + [
    'parent_id',
    'note',
    'created_at',
    'updated_at',
    'project_id',
]


@cliutils.arg('--fields',
              nargs='+',
              metavar='<fields>',
              default=DEFAULT_DEVICE_FIELDS,
              help='Space-separated list of fields to display. '
                   'Only these fields will be fetched from the server. '
                   'This cannot be combined with --detail.')
@cliutils.arg('--detail',
              action='store_true',
              default=False,
              help='Retrieve and show all detail about devices in listing.')
@cliutils.arg('--all',
              action='store_true',
              default=False,
              help='Retrieve and show all devices. This will override '
                   'the provided value for --limit and automatically '
                   'retrieve each page of results.')
@cliutils.arg('--sort-key',
              metavar='<field>',
              help='Device field that will be used for sorting.')
@cliutils.arg('--sort-dir',
              metavar='<direction>',
              default='asc',
              choices=('asc', 'desc'),
              help='Sort direction: "asc" (default) or "desc".')
@cliutils.arg('--limit',
              metavar='<limit>',
              type=int,
              help='Maximum number of devices to return.')
@cliutils.arg('--marker',
              metavar='<marker>',
              default=None,
              help='ID of the device to use to resume listing devices.')
@cliutils.arg('--cloud',
              metavar='<cloud>',
              type=int,
              help='ID of the cloud that the device belongs to.')
@cliutils.arg('-r', '--region',
              metavar='<region>',
              type=int,
              help='ID of the region that the device belongs to.')
@cliutils.arg('-c', '--cell',
              metavar='<cell>',
              type=int,
              help='Integer ID of the cell that contains '
                   'the desired list of devices.')
@cliutils.arg('--parent',
              metavar='<parent>',
              type=int,
              help='Parent ID of required devices.')
@cliutils.arg('--descendants',
              default=False,
              action='store_true',
              help='When parent is also specified, include all descendants.')
@cliutils.arg('--active',
              metavar='<active>',
              choices=("true", "false"),
              help='Filter devices by their active state.')
def do_device_list(cc, args):
    """List all devices."""
    params = {}
    if args.limit is not None:
        if args.limit < 0:
            raise exc.CommandError('Invalid limit specified. Expected '
                                   'non-negative limit, got {0}'
                                   .format(args.limit))
        params['limit'] = args.limit
    if args.all is True:
        params['limit'] = 100

    if args.detail:
        if args.fields and args.fields == DEFAULT_DEVICE_FIELDS:
            args.fields = DEVICE_FIELDS
        else:
            raise exc.CommandError(
                'Cannot specify both --fields and --detail.'
            )
        params['detail'] = args.detail

    fields = args.fields
    for field in fields:
        if field not in DEVICE_FIELDS:
            raise exc.CommandError(
                'Invalid field "{}"'.format(field)
            )

    sort_key = args.sort_key and args.sort_key.lower()
    if sort_key is not None:
        if sort_key not in DEVICE_FIELDS:
            raise exc.CommandError(
                '{0} is an invalid key for sorting,  valid values for '
                '--sort-key are: {1}'.format(
                    args.sort_key, DEVICE_FIELDS
                )
            )
        params['sort_keys'] = sort_key
    params['sort_dir'] = args.sort_dir
    params['marker'] = args.marker
    params['autopaginate'] = args.all
    if args.parent:
        params['parent_id'] = args.parent
    params['descendants'] = args.descendants
    if args.cloud:
        params['cloud_id'] = args.cloud
    if args.region:
        params['region_id'] = args.region
    if args.cell:
        params['cell_id'] = args.cell
    if args.active:
        params['active'] = args.active

    devices_list = cc.devices.list(**params)
    args.formatter.configure(fields=fields).handle(devices_list)