# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from ..common import SpreadsheetTestCommon

from odoo.tests import tagged, loaded_demo_data
from odoo.tests.common import HttpCase
from odoo.tools import file_open, misc

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install")
class TestSpreadsheetOpenPivot(SpreadsheetTestCommon, HttpCase):
    @classmethod
    def setUpClass(cls):
        super(TestSpreadsheetOpenPivot, cls).setUpClass()
        data_path = misc.file_path('documents_spreadsheet/demo/files/res_partner_spreadsheet.json')
        # Avoid interference from the demo data which rename the admin user
        cls.env['res.users'].browse(2).write({"name": "AdminDude"})
        with file_open(data_path, 'rb') as f:
            cls.spreadsheet = cls.env["documents.document"].create({
                "handler": "spreadsheet",
                "folder_id": cls.folder.id,
                "raw": f.read(),
                "name": "Res Partner Test Spreadsheet"
            })

    def test_01_spreadsheet_open_pivot_as_admin(self):
        # The test file is relying on demo data with hardcoded ids
        if not loaded_demo_data(self.env):
            _logger.warning("This test relies on demo data. To be rewritten independently of demo data for accurate and reliable results.")
            return
        self.start_tour("/web", "spreadsheet_open_pivot_sheet", login="admin")

    def test_01_spreadsheet_open_pivot_as_user(self):
        # The test file is relying on demo data with hardcoded ids
        if not loaded_demo_data(self.env):
            _logger.warning("This test relies on demo data. To be rewritten independently of demo data for accurate and reliable results.")
            return
        self.start_tour("/web", "spreadsheet_open_pivot_sheet", login="spreadsheetDude")
