from odoo import api, models


class ITPurchaseOrderReport(models.AbstractModel):
    _name = 'report.it_procurement.report_itpurchaseorder'
    _description = 'IT Purchase Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['purchase.order'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'purchase.order',
            'docs': docs,
        } 