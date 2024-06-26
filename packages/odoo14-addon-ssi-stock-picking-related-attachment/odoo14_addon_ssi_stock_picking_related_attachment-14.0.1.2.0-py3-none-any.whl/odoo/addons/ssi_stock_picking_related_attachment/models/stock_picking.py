# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = [
        "stock.picking",
        "mixin.related_attachment",
    ]
    _related_attachment_create_page = True

    @api.onchange("picking_type_category_id")
    def onchange_related_attachment_template_id(self):
        self.related_attachment_template_id = False
        if self.picking_type_category_id:
            self.related_attachment_template_id = (
                self._get_template_related_attachment()
            )

    @api.model_create_multi
    def create(self, vals_list):
        _super = super(StockPicking, self)
        pickings = _super.create(vals_list)
        pickings.onchange_related_attachment_template_id()
        return pickings
