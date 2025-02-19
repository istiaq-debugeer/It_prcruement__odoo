from odoo import http
from odoo.http import request
import logging


_logger = logging.getLogger(__name__)


class ITProcurementController(http.Controller):
    @http.route(
        "/it_procurement/create_purchase_order", type="http", auth="user", website=True
    )
    def create_purchase_order(self, **kwargs):
        _logger.info("✅ create_purchase_order route is being accessed")
        # Render a form for creating a purchase order
        return request.render("it_procurement.create_purchase_order")

    @http.route("/it_procurement/save_purchase_order", type="json", auth="user")
    def save_purchase_order(self, **kwargs):
        # Get data from the request
        partner_id = kwargs.get("partner_id")
        order_line = kwargs.get("order_line", [])

        # Create the purchase order
        purchase_order = request.env["purchase.order"].create(
            {
                "partner_id": partner_id,
                "order_line": [(0, 0, line) for line in order_line],
            }
        )

        return {
            "status": "success",
            "message": "Purchase order created successfully",
            "order_id": purchase_order.id,
        }

    @http.route(
        "/it_procurement/purchase_orders", type="http", auth="user", website=True
    )
    def purchase_orders(self, **kwargs):
        purchase_orders = request.env["purchase.order"].search([])
        values = {
            "purchase_orders": purchase_orders,
        }
        return request.render("it_procurement.purchase_orders_template", values)

    @http.route(
        '/it_procurement/purchase_order/<model("purchase.order"):order>',
        type="http",
        auth="user",
        website=True,
    )
    def purchase_order_detail(self, order, **kwargs):
        values = {
            "order": order,
        }
        return request.render("it_procurement.purchase_order_detail_template", values)

    @http.route(
        "/it_procurement/approve_purchase/<int:order_id>", type="json", auth="user"
    )
    def approve_purchase(self, order_id):
        order = request.env["purchase.order"].browse(order_id)
        if request.env.user.has_group("it_procurement.group_coo"):
            order.confirm_purchase_order()
            return {"status": "success", "message": "Purchase order confirmed by COO"}
        elif request.env.user.has_group("it_procurement.group_md"):
            order.approved_by_md = True
            return {"status": "success", "message": "Purchase order approved by MD"}
        return {"status": "error", "message": "Unauthorized action"}

    @http.route("/my/purchase_orders", type="http", auth="user", website=True)
    def vendor_purchase_orders(self, **kwargs):
        if not request.env.user.partner_id:
            return request.redirect("/my")

        purchase_orders = request.env["purchase.order"].search(
            [("partner_id", "=", request.env.user.partner_id.id)]
        )

        values = {
            "purchase_orders": purchase_orders,
        }
        return request.render("it_procurement.vendor_portal_orders", values)
