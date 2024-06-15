# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.account.tests.common import AccountTestInvoicingHttpCommon
from odoo.exceptions import UserError
from odoo.tests.common import tagged


@tagged('post_install', '-at_install')
class TestMerge(AccountTestInvoicingHttpCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        if 'account.account' not in cls.env:
            cls.skipTest(cls, "`account` module not installed")

        cls.account_sale_a = cls.company_data['default_account_receivable']
        cls.account_sale_b = cls.env['account.account'].create({
            'code': '40002',
            'name': 'Account Sale B',
            'account_type': 'asset_receivable',
            'reconcile': True,
        })

    def _enable_merge(self, model_name):
        self.res_model_id = self.env['ir.model'].search([('model', '=', model_name)])
        self.res_model_id.action_merge_contextual_enable()
        self.model_id = self.env['data_merge.model'].create({
            'name': model_name,
            'res_model_id': self.res_model_id.id,
        })

    def test_merge_account(self):
        """
        Test that we cannot merge accounts.
        """
        self._enable_merge('account.account')

        data_merge_group = self.env['data_merge.group'].create({
            'model_id': self.model_id.id,
            'res_model_id': self.res_model_id.id,
            'record_ids': [
                (0, 0, {
                    'res_id': self.account_sale_a.id,
                    'is_master': True,
                }),
                (0, 0, {
                    'res_id': self.account_sale_b.id,
                }),
            ],
        })

        # use to replicate information sent from JS call `_onMergeClick`
        group_records = {str(data_merge_group.id): data_merge_group.record_ids.ids}
        with self.assertRaises(UserError, msg="You cannot merge accounts."):
            self.env['data_merge.group'].merge_multiple_records(group_records)

    def test_merge_partner_in_hashed_entries(self):
        """
        Test that we cannot merge partners used in hashed entries
        """
        self._enable_merge('res.partner')
        self.company_data['default_journal_sale'].restrict_mode_hash_table = True

        # todo: investigate why it is needed to init the sequence to avoid hash constraint error
        self.init_invoice("out_invoice", self.partner_b, "2023-07-22", amounts=[1000], post=False)
        move = self.init_invoice("out_invoice", self.partner_b, "2023-07-22", amounts=[1000], post=False)
        move.action_post()

        # The integrity check should work
        integrity_check = move.company_id._check_hash_integrity()['results'][0]
        self.assertRegex(integrity_check['msg_cover'], 'All entries are hashed.*')

        data_merge_group = self.env['data_merge.group'].create({
            'model_id': self.model_id.id,
            'res_model_id': self.res_model_id.id,
            'record_ids': [
                (0, 0, {
                    'res_id': self.partner_a.id,
                    'is_master': True,
                }),
                (0, 0, {
                    'res_id': self.partner_b.id,
                }),
            ],
        })

        # use to replicate information sent from JS call `_onMergeClick`
        group_records = {str(data_merge_group.id): data_merge_group.record_ids.ids}
        with self.assertRaises(UserError, msg="Records that are used as fields in hashed entries cannot be merged."):
            self.env['data_merge.group'].merge_multiple_records(group_records)
