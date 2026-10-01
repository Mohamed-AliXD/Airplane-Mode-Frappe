import frappe


def get_context(context):
    context.no_cache = 1
    context.shops = frappe.get_all(
        "Shop",
        fields=["name", "shop_number", "shop_name", "airport", "status"],
        order_by="airport, shop_number",
    )
