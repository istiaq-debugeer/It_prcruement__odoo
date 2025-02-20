from odoo import api, fields, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    equipment_type = fields.Char(string="Equipment Type")
    priority = fields.Selection(
        [("low", "Low"), ("medium", "Medium"), ("high", "High")],
        string="Priority",
        default="medium",
    )
    requested_by = fields.Many2one("res.users", string="Requested By")
    expected_delivery_date = fields.Date(string="Expected Delivery Date")
    technical_specifications = fields.Text(string="Technical Specifications")
    confirmed_by_coo = fields.Boolean(string="Confirmed by COO", default=False)
    approved_by_md = fields.Boolean(string="Approved by MD", default=False)
    requires_md_approval = fields.Boolean(
        string="Requires MD Approval", compute="_compute_requires_md_approval"
    )

    @api.depends("amount_total")
    def _compute_requires_md_approval(self):
        for record in self:
            record.requires_md_approval = record.amount_total > 50000

    def confirm_purchase_order(self):
        if not self.env.user.has_group("it_procurement.group_coo"):
            raise UserError("Only COO can confirm purchase orders.")
        self.confirmed_by_coo = True
        if self.requires_md_approval and not self.approved_by_md:
            return {
                "warning": {
                    "title": "MD Approval Required",
                    "message": "This purchase order requires MD approval as it exceeds 50,000 Taka.",
                }
            }
        self.button_confirm()

    def approve_md(self):
        if not self.env.user.has_group("it_procurement.group_md"):
            raise UserError("Only MD can approve purchase orders.")
        self.approved_by_md = True
        if self.confirmed_by_coo:
            self.button_confirm()

    def send_vendor_notification(self):
        template = self.env.ref("it_procurement.email_template_purchase_order")
        self.message_post_with_template(template.id)
