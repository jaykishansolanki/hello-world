# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api, exceptions
# from odoo.exceptions import ValidationError


class EmployeeEmployee(models.Model):
    _name = 'employee.employee'

    name = fields.Char(string="Employee Name")
    lastname = fields.Char(string="Last Name")
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], default='male')
    state = fields.Selection([('draft', 'Active'), ('confirm', 'Onleave'), ('invalid', 'Inactive')], default='draft')       
    nationality = fields.Char(string="Nationality")
    joining_date = fields.Date(string="Date of Join")
    leaving_date = fields.Date(string="Date of Leave")
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", required=True)
    salary = fields.Float(digits=(7, 2), string="salary")
    department_id = fields.Many2one('employee.department', ondelete='set null', string='Department')
    description = fields.Text(string="Description")
    tax = fields.Float()#compute='tax_compute'
    image = fields.Binary("Image", attachment=True, help="This field holds the image used as image for the employee, limited to 1024x1024px.")
    emp_id = fields.Char(string='Employee ID', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))

    _sql_constraints = [
        # ('name_check',
        #  'CHECK(name != '')',
        #  "The name should not be blank"),

        ('name_unique',
         'UNIQUE(name)',
         "Employee name must be unique --> SQL constraints"),
    ]

    # @api.depends('salary')
    # def tax_compute(self):
    #     # print "self...", self, len(self)
    #     self.tax = self.salary * 0.15

    @api.model
    def create(self, vals):

        print vals.get('emp_id')
        if vals.get('emp_id', 'New') == 'New':
            print "if block for sequence is execute"
            vals['emp_id'] = self.env['ir.sequence'].next_by_code('employee.employee') or 'New'

        # print "vals----->", vals.get('name')
        # print "vals----->", vals.get('lastname')
        if vals.get('name') == vals.get('lastname'):
            raise exceptions.ValidationError("Lastname is different than Name!!")
        if vals.get('salary') <= 0:
            # raise exceptions.ValidationError("Salary must be positive!")
            vals['salary'] = 10000

        # print "---->", vals
        return super(EmployeeEmployee, self).create(vals)

    @api.multi
    def write(self, vals):
        print "vals------->", vals
        for name, value in vals.items():
            # print "name is: ", name
            # print "value is: ", value
            vals[name] = value
        # (1, self.env['EmployeeEmployee'], vals)
        # print "Vals are: ", vals
        super(EmployeeEmployee, self).write(vals)
        return True

    @api.multi
    def unlink(self):
        # Filter to check employee state if is active(draft) we can't delete it.
        #raise exceptions.ValidationError("You can't delete active user")
        final_list = list(filter(lambda emp: emp['state'] != 'draft', self))
        print(final_list)

        for emp in final_list:
            print "emp", emp
            super(EmployeeEmployee, emp).unlink()

        # if self.state == 'draft':
        #     print "if block executed..."
        #     raise exceptions.ValidationError("You can't delete active user")
        # else:
        #     print "Else method called"
        #     super(EmployeeEmployee, self).unlink()

    # @api.depends('name')
    # def compute_last_name(self):
    #     self.lastname = self.name + str(1)

    #methods for workflow status
    @api.multi
    def action_active(self):
        self.state = 'draft'

    @api.multi
    def action_onleave(self):
        self.state = 'confirm'

    @api.multi
    def action_inactive(self):
        self.state = 'invalid'

    @api.constrains('age')
    def _check_adult(self):
        if self.age < 18:
            raise exceptions.ValidationError("You aren't adult, your age is: %s" % self.age)

    @api.onchange('salary')
    def count_tax(self):
        self.tax = self.salary * .15


class EmployeeDepartment(models.Model):
    _name = 'employee.department'

    name = fields.Char(String="Department Name", required=True)
    code = fields.Char(String="Department Code")
    dept_head_id = fields.Many2one('res.partner', string="Department head", domain=['|',('dept_head', '=', True),('category_id.name', 'ilike', "Employee")]) #domain=[('name', 'ilike', 'agrolait')
    employee_ids = fields.One2many('employee.employee', 'department_id', string="Employee List")
    team_ids = fields.Many2many('res.partner', string='Deptartment Team')
    tag_id = fields.Many2one('res.partner.category',string="Tag")
    average_salary = fields.Float(string='Average Salary', compute='avg_salary')
    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))

    @api.model
    def create(self, vals):

        print vals.get('sequence')
        if vals.get('sequence', 'New') == 'New':
            print "if block for sequence is execute"
            vals['sequence'] = self.env['ir.sequence'].next_by_code('employee.department') or 'New'

        return super(EmployeeDepartment, self).create(vals)

    @api.onchange('dept_head_id')
    def set_dept_head(self):
        if self.dept_head_id:
            part = self.env['res.partner'].browse(self.dept_head_id.id)
            part.write({'dept_head': True})

    @api.depends('employee_ids')
    def avg_salary(self):
        avg_salary = 0
        for empid in self.employee_ids:
            avg_salary += empid.salary
        print "self.length is= ",len(self.employee_ids)
        if self.average_salary != 0:
            self.average_salary = avg_salary / len(self.employee_ids)


class Partner(models.Model):
    _inherit = 'res.partner'

    dept_head = fields.Boolean(string="Department head")

    # round_total = fields.Monetary(string='Round Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')

    # @api.depends('order_line.price_total')
    # def _amount_all(self):

    #     for order in self:
    #         amount_untaxed = amount_tax = 0.0
    #         for line in order.order_line:
    #             amount_untaxed += line.price_subtotal
    #             amount_tax += line.price_tax
    #         order.update({
    #             # print "amount_untaxed is---> ", amount_untaxed
    #             # print "amount_tax is---> ", amount_tax
    #             self.amount_untaxed = amount_untaxed,
    #             self.amount_tax=amount_tax,
    #             self.amount_total=amount_untaxed + amount_tax,
    #             self.round_total=(self.amount_untaxed + self.amount_tax)-round((self.amount_untaxed + self.amount_tax))
    #         })

    #     return super(SaleOrder, self)._amount_all()
