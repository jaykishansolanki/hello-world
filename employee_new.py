# -*- coding: utf-8 -*-

from odoo import api, fields , models

class Employee(models.Model):
    _name = 'employee.employee'

    name = fields.Char(string = "Employee Name")
    lastname = fields.Char(string = "Last Name")
    sex = fields.Selection([('male' , 'Male'), ('female', 'Female')], default='male')
    state = fields.Selection([('draft','Active'), ('confirm', 'Onleave'), ('invalid', 'Inactive')], default='draft')
    nationality = fields.Char(string ="Nationality")
    joining_date = fields.Char(string ="Joining Date")
    leaving_date = fields.Char(string ="Joining Date")
    dob = fields.Char("Date of Birth")
    age = fields.Integer(string ="Age", required=True)
    salary = fields.Float(digit=(7, 2), string="Salary")
    department_id = fields.Many2one('emplloyee.department', ondetele='set null', string="Dapartment")
    description = fields.Text(string="Description")
    tax = fields.Float()
    image = fields.Binary("Image", attechment=True, help="Please Upload Image")
    