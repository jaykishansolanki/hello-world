# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models


class PurchaseRound(models.Model):
    _inherit = "purchase.order"

    amount_round = fields.Monetary(string='Amount Round', store=True, readonly=True, compute="_amount_all", track_visibility='always')

    @api.depends('order_line.price_total', 'amount_total')
    def _amount_all(self):
        res = super(PurchaseRound, self)._amount_all()
        for order in self:
              order.update({
                 'amount_round':  round(order.amount_untaxed + order.amount_tax) - (order.amount_untaxed + order.amount_tax),
                 'amount_total': round(order.amount_untaxed + order.amount_tax),
                })
        return res