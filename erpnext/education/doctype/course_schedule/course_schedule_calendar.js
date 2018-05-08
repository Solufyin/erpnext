frappe.views.calendar["Course Schedule"] = {
	field_map: {
		// from_datetime and to_datetime don't exist as docfields but are used in onload
		"start": "from_datetime",
		"end": "to_datetime",
		"id": "name",
		"title": "course",
		"allDay": "allDay"
	},
	gantt: false,
<<<<<<< HEAD
	order_by: "schedule_date",
=======
	order_by: "from_time",
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "student_group",
			"options": "Student Group",
			"label": __("Student Group")
		},
		{
			"fieldtype": "Link",
			"fieldname": "course",
			"options": "Course",
			"label": __("Course")
		},
		{
			"fieldtype": "Link",
			"fieldname": "instructor",
			"options": "Instructor",
			"label": __("Instructor")
		},
		{
			"fieldtype": "Link",
			"fieldname": "room",
			"options": "Room",
			"label": __("Room")
		}
	],
	get_events_method: "erpnext.education.api.get_course_schedule_events"
}
