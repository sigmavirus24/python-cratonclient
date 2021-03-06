# -*- coding: utf-8 -*-

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
"""Regions manager code."""
from cratonclient import crud


class Cell(crud.Resource):
    """Representation of a Region."""

    pass


class CellManager(crud.CRUDClient):
    """A manager for cells."""

    key = 'cell'
    base_path = '/cells'
    resource_class = Cell
    region_id = 0

    def __init__(self, region_id, session, url):
        """Initialize our CellManager object with region, session, and url."""
        super(CellManager, self).__init__(session, url)
        self.region_id = region_id

    def list(self, **kwargs):
        """Retrieve the cells in a specific region."""
        kwargs['region_id'] = self.region_id
        return super(CellManager, self).list(**kwargs)

    def create(self, **kwargs):
        """Create a cell in a specific region."""
        kwargs['region_id'] = self.region_id
        return super(CellManager, self).create(**kwargs)


CELL_FIELDS = {
    'id': 'ID',
    'region_id': 'Region ID',
    'project_id': 'Project ID',
    'name': 'Name',
    'note': 'Note',
    'created_at': 'Created At',
    'update_at': 'Updated At'
}
