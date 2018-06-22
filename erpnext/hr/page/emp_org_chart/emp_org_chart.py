from __future__ import unicode_literals
import frappe
from frappe import _



@frappe.whitelist()
def get_parent_employees():
	print ":::get_parent_employees:::CALL::::"
	parent_employees = frappe.get_all('Employee', filters=[
			['reports_to', '=', '']])
	print "\n parent_employees ::::::::::::", parent_employees
# 	parent_employees :::::::::::: [{u'name': u'EMP/00002'}, {u'name': u'EMP/00003'}]

	parent_child_lst = {}
	for parent_employee in parent_employees:
		child_employees = frappe.get_list('Employee', filters=[
			['reports_to', '=', parent_employee['name']]])
		if not parent_child_lst:
			parent_child_lst.update({str(parent_employee['name']): []})
		if parent_child_lst and not parent_child_lst.get(parent_employee['name'], False):
			parent_child_lst.update({str(parent_employee['name']): []})
		if child_employees:
			for child_employee in child_employees:
				print "\n parent_child_lst ::::::1:::::", parent_child_lst
				print "\n child_employee :::::::2::::", child_employee, child_employee['name']
				if child_employee:
					if parent_child_lst:
						print "\n parent_child_lst.get(str(parent_employee['name'])) :::::::", parent_employee['name'], parent_child_lst, parent_child_lst.get(str(parent_employee['name']))
						print "@@@@@@@@@@@@@@@@@@@@@@@@@@@", str(child_employee['name'])
						parent_child_lst.get(str(parent_employee['name'])).append(str(child_employee['name']))
	print "\n parent_child_lst ::::::final::::::", parent_child_lst
# 	test = {'A': ['C', 'B'],'B': ['D', 'E']}
	return parent_child_lst

@frappe.whitelist()
def get_employee_data():
	print ":::get_employee_data:::SUCCESSfully Call:::::::"
	all_employees = frappe.get_all('Employee',
		filters={'status': 'Active'},
		fields = ["name"],
		order_by="lft, rgt")
	print "\n all_employees ::::::::::::", all_employees
	return all_employees

# @frappe.whitelist()
# def get_parent_children():
# 	filters = [['company', '=', company]]
# 	fields = ['name as value', 'employee_name as title']
# 
# 	if is_root:
# 		parent = ''
# 		print "parent::::::::::::::",parent
# 		
# 	if parent and company and parent!=company:
# 		filters.append(['reports_to', '=', parent])
# 		
# 	else:
# 		filters.append(['reports_to', '=', ''])
	
# 	employees = frappe.get_list(doctype, fields=fields,
# 		filters=filters, order_by='name')
# 	
# 	print "employee list:::::::::::",employees
# 
# 	for employee in employees:
# 		is_expandable = frappe.get_all(doctype, filters=[
# 			['reports_to', '=', employee.get('value')]
# 		])
# 		employee.expandable = 1 if is_expandable else 0

# 	employees = frappe.db.sql("select name,reports_to from `tabEmployee`")
# 	print "::::::::::::emp:::::::::",employees
# 	
# 	return employees


