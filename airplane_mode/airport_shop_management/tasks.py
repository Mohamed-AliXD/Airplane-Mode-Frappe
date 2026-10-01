import frappe
from frappe.utils import get_first_day, getdate, today


def send_rent_reminders():
    # Stop if reminders are switched off in Shop Settings
    if not frappe.db.get_single_value("Shop Settings", "enable_rent_reminders"):
        return

    due_date = get_first_day(getdate(today()))

    contracts = frappe.get_all(
        "Shop Contract",
        filters={"status": "Active", "expiry_date": [">=", due_date]},
        fields=["name", "tenant", "rent_amount"],
    )

    for contract in contracts:
        # Skip if this month's payment already exists
        if frappe.db.exists("Rent Payment", {"contract": contract.name, "due_date": due_date}):
            continue

        payment = frappe.get_doc(
            {
                "doctype": "Rent Payment",
                "contract": contract.name,
                "due_date": due_date,
                "amount": contract.rent_amount,
                "status": "Unpaid",
            }
        ).insert(ignore_permissions=True)

        email = frappe.db.get_value("Shop Tenant", contract.tenant, "email")
        if email:
            frappe.sendmail(
                recipients=[email],
                subject="Rent due this month",
                message=f"Your rent of {contract.rent_amount} is due. Reference: {payment.name}.",
            )
