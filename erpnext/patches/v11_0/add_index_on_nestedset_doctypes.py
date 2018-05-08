# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe

def execute():
	frappe.reload_doc("agriculture", "doctype", "land_unit")
	for dt in ("Account", "Cost Center", "File", "Employee", "Land Unit", "Task", "Customer Group", "Sales Person", "Territory"):
<<<<<<< HEAD
		frappe.reload_doctype(dt)
=======
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
		frappe.get_doc("DocType", dt).run_module_method("on_doctype_update")