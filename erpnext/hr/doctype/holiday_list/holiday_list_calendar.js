// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Holiday List"] = {
	field_map: {
<<<<<<< HEAD
		"start": "from_date",
		"end": "to_date",
=======
		"start": "holiday_date",
		"end": "holiday_date",
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
		"id": "name",
		"title": "description",
		"allDay": "allDay"
	},
	get_events_method: "erpnext.hr.doctype.holiday_list.holiday_list.get_events",
	filters: [
		{
			'fieldtype': 'Link',
			'fieldname': 'holiday_list',
			'options': 'Holiday List',
			'label': __('Holiday List')
		}
	]
}
