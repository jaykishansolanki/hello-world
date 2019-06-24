# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sale Purchase Round',
    'version': '1.1',
    'summary': 'Sale and Purchase Round',
    'sequence': 30,
    'description': """
            Sale and Purchase Round Task
    """,
    'category': 'sales',
    'website': 'https://www.odoo.com',
    'depends': ['base', 'l10n_in', 'account_accountant', 'sale', 'purchase'],
    'data': [
        'views/sale_round_view.xml',
        ], 
}
