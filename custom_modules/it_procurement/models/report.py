from odoo import fields, models


class ITProcurementReport(models.Model):
    _name = 'it.procurement.report'
    _description = 'IT Procurement Report'

    name = fields.Char(string='Report Name')
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    total_orders = fields.Integer(string='Total Orders')
    total_amount = fields.Float(string='Total Amount') 