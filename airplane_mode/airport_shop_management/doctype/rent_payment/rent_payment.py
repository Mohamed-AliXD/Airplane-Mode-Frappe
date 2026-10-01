# Copyright (c) 2026, mohamedali456@gmail.com and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe.model.document import Document
from frappe.utils import today


class RentPayment(Document):
    def before_save(self):
        if self.status == "Paid" and not self.paid_on:
            self.paid_on = today()
