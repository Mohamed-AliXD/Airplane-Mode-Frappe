import frappe


def get_context(context):
    context.no_cache = 1
    name = frappe.form_dict.name
    if not name or not frappe.db.exists("Shop", name):
        frappe.throw("Shop not found", frappe.DoesNotExistError)
    context.shop = frappe.get_doc("Shop", name)
