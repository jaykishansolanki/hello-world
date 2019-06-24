# -*- coding: utf-8 -*-
{
	'name': 'School',
	'version': '12.0.1.0.0',
	'summary': 'Record Student Information',
	'category': 'Tools',
	'author': 'JAO',
	'maintainer': 'odoo',
	'company': 'odoo india',
	'website': 'https://www.odoo.com',
	'depends': ['base'],
	'data': [
    	'security/ir.model.access.csv',
    	'views/student_views.xml',
    	# 'views/employee_views.xml'
	],
	'images': [],
	'license': 'AGPL-3',
	'installable': True,
	'application': False,
	'auto_install': False,
}