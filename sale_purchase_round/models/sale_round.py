# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models


class SalesRound(models.Model):
    _inherit = "sale.order"

    amount_round = fields.Monetary(string='Amount Round', store=True, readonly=True, compute="_amount_all", track_visibility='always')

    @api.depends('amount_total')
    def _amount_all(self):
        res = super(SalesRound, self)._amount_all()
        for order in self:
            order.update({
                'amount_total': round(order.amount_untaxed + order.amount_tax),
                'amount_round':  round(order.amount_untaxed + order.amount_tax) - (order.amount_untaxed + order.amount_tax),
            })
        return res
