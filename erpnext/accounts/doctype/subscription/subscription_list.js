frappe.listview_settings['Subscription'] = {
<<<<<<< HEAD
	get_indicator: function(doc) {
		if(doc.status === 'Trialling') {
			return [__("Trialling"), "green"];
		} else if(doc.status === 'Active') {
			return [__("Active"), "green"];
		} else if(doc.status === 'Past Due Date') {
			return [__("Past Due Date"), "orange"];
		} else if(doc.status === 'Unpaid') {
			return [__("Unpaid"), "red"];
		} else if(doc.status === 'Cancelled') {
			return [__("Cancelled"), "darkgrey"];
=======
	add_fields: ["next_schedule_date"],
	get_indicator: function(doc) {
		if(doc.disabled) {
			return [__("Disabled"), "red"];
		} else if(doc.next_schedule_date >= frappe.datetime.get_today() && doc.status != 'Stopped') {
			return [__("Active"), "green"];
		} else if(doc.docstatus === 0) {
			return [__("Draft"), "red", "docstatus,=,0"];
		} else if(doc.status === 'Stopped') {
			return [__("Stopped"), "red"];
		} else {
			return [__("Expired"), "darkgrey"];
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
		}
	}
};