# -*- coding: utf-8 -*-
import time
from datetime import datetime
from odoo import models, fields, api, exceptions
# from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        po_lines = []
        for line in self.order_line:
            product_id = line.product_id
            qty = self.env['stock.quant'].search([('product_id', '=', product_id.id)], order='id desc', limit=1)
            rest_qty = 0
            if qty:
                quantity = qty.quantity
                rest_qty = line.product_uom_qty - quantity
            po_lines.append((0, 0, {
                'name': line.name,
                'product_id': line.product_id.id,
                'product_qty': rest_qty,
                'product_uom': line.product_uom.id,
                'date_planned': time.strftime('%Y-%m-%d'),
                'price_unit': line.price_unit,
            }))
            self.env['purchase.order'].create({
            'partner_id': self.partner_id.id,
            'order_line': po_lines,
            })   
        return res
