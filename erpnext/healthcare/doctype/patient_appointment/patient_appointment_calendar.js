
frappe.views.calendar["Patient Appointment"] = {
	field_map: {
<<<<<<< HEAD
		"start": "appointment_date",
		"end": "appointment_datetime",
=======
		"start": "start",
		"end": "end",
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
		"id": "name",
		"title": "patient",
		"allDay": "allDay",
		"eventColor": "color"
	},
<<<<<<< HEAD
	order_by: "appointment_date",
=======
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
	gantt: true,
	get_events_method: "erpnext.healthcare.doctype.patient_appointment.patient_appointment.get_events",
	filters: [
		{
			'fieldtype': 'Link',
			'fieldname': 'physician',
			'options': 'Physician',
			'label': __('Physician')
		},
		{
			'fieldtype': 'Link',
			'fieldname': 'patient',
			'options': 'Patient',
			'label': __('Patient')
		},
		{
			'fieldtype': 'Link',
			'fieldname': 'appointment_type',
			'options': 'Appointment Type',
			'label': __('Appointment Type')
		},
		{
			'fieldtype': 'Link',
			'fieldname': 'department',
			'options': 'Medical Department',
			'label': __('Department')
		},
		{
			'fieldtype': 'Select',
			'fieldname': 'status',
			'options': 'Scheduled\nOpen\nClosed\nPending',
			'label': __('Status')
		}
	]
};
