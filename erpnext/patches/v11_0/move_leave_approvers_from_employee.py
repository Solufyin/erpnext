import frappe
from frappe import _

def execute():
<<<<<<< HEAD
	frappe.reload_doc("hr", "doctype", "department_approver")
	frappe.reload_doc("hr", "doctype", "employee")
	frappe.reload_doc("hr", "doctype", "department")
=======
	frappe.reload_doc("hr", "doctype", "employee")
	frappe.reload_doc("hr", "doctype", "department")
	frappe.reload_doc("hr", "doctype", "employee_leave_approver")
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825

	approvers = frappe.db.sql("""select distinct app.leave_approver, emp.department from
	`tabEmployee Leave Approver` app, `tabEmployee` emp
		where app.parenttype = 'Employee'
		and emp.name = app.parent
		""", as_dict=True)
	for record in approvers:
		if record.department:
<<<<<<< HEAD
			frappe.db.sql("""update `tabDepartment Approver` set parenttype = '{0}',
				parent = '{1}' and parentfield = 'leave_approver' where approver = '{2}'"""
=======
			frappe.db.sql("""update `tabDepartment Approver` app set app.parenttype = '{0}',
				app.parent = '{1}' and parentfield = 'leave_approver' where app.leave_approver = '{2}'"""
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
				.format(_('Department'), record.department, record.leave_approver))
