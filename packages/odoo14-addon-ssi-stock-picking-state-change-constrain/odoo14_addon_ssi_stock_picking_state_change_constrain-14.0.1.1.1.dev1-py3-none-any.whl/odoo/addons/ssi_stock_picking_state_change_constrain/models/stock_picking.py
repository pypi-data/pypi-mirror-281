# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

from odoo import api, models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = [
        "stock.picking",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    _status_check_create_page = True

    @api.onchange("picking_type_id")
    def onchange_status_check_template_id(self):
        self.status_check_template_id = False
        if self.picking_type_id:
            self.status_check_template_id = self._get_template_status_check()

    @api.model_create_multi
    def create(self, vals_list):
        _super = super(StockPicking, self)
        pickings = _super.create(vals_list)
        pickings.onchange_status_check_template_id()
        return pickings
