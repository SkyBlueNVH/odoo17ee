from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _extend_with_attachments(self, attachments, new=False):
        l10n_it_attachments = attachments.filtered(lambda rec: rec._is_l10n_it_edi_import_file())
        attachments = attachments - l10n_it_attachments

        return (super(AccountMove, self)._extend_with_attachments(attachments, new)
            or super(AccountMove, self.with_context(
                disable_onchange_name_predictive=True,
            ))._extend_with_attachments(l10n_it_attachments, new)
        )
