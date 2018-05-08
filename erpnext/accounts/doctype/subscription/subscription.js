<<<<<<< HEAD
// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Subscription', {
	refresh: function(frm) {
		if(!frm.is_new()){
			if(frm.doc.status !== 'Cancelled'){
				frm.add_custom_button(
					__('Cancel Subscription'),
					() => frm.events.cancel_this_subscription(frm)
				);
				frm.add_custom_button(
					__('Fetch Subscription Updates'),
					() => frm.events.get_subscription_updates(frm)
				);
			}
			else if(frm.doc.status === 'Cancelled'){
				frm.add_custom_button(
					__('Restart Subscription'),
					() => frm.events.renew_this_subscription(frm)
				);
			}
		}
	},

	cancel_this_subscription: function(frm) {
		const doc = frm.doc;
		frappe.confirm(
			__('This action will stop future billing. Are you sure you want to cancel this subscription?'),
			function() {
				frappe.call({
					method:
					"erpnext.accounts.doctype.subscription.subscription.cancel_subscription",
					args: {name: doc.name},
					callback: function(data){
						if(!data.exc){
							frm.reload_doc();
						}
					}
				});
			}
		);
	},

	renew_this_subscription: function(frm) {
		const doc = frm.doc;
		frappe.confirm(
			__('You will lose records of previously generated invoices. Are you sure you want to restart this subscription?'),
			function() {
				frappe.call({
					method:
					"erpnext.accounts.doctype.subscription.subscription.restart_subscription",
					args: {name: doc.name},
					callback: function(data){
						if(!data.exc){
							frm.reload_doc();
						}
					}
				});
			}
		);
	},

	get_subscription_updates: function(frm) {
		const doc = frm.doc;
		frappe.call({
			method:
			"erpnext.accounts.doctype.subscription.subscription.get_subscription_updates",
			args: {name: doc.name},
			freeze: true,
			callback: function(data){
				if(!data.exc){
=======
// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Subscription', {
	setup: function(frm) {
		frm.fields_dict['reference_doctype'].get_query = function(doc) {
			return {
				query: "erpnext.accounts.doctype.subscription.subscription.subscription_doctype_query"
			};
		};

		frm.fields_dict['reference_document'].get_query = function() {
			return {
				filters: {
					"docstatus": 1,
					"subscription": ''
				}
			};
		};

		frm.fields_dict['print_format'].get_query = function() {
			return {
				filters: {
					"doc_type": frm.doc.reference_doctype
				}
			};
		};
	},

	refresh: function(frm) {
		if(frm.doc.docstatus == 1) {
			let label = __('View {0}', [frm.doc.reference_doctype]);
			frm.add_custom_button(__(label),
				function() {
					frappe.route_options = {
						"subscription": frm.doc.name,
					};
					frappe.set_route("List", frm.doc.reference_doctype);
				}
			);

			if(frm.doc.status != 'Stopped') {
				frm.add_custom_button(__("Stop"),
					function() {
						frm.events.stop_resume_subscription(frm, "Stopped");
					}
				);
			}

			if(frm.doc.status == 'Stopped') {
				frm.add_custom_button(__("Resume"),
					function() {
						frm.events.stop_resume_subscription(frm, "Resumed");
					}
				);
			}
		}
	},

	stop_resume_subscription: function(frm, status) {
		frappe.call({
			method: "erpnext.accounts.doctype.subscription.subscription.stop_resume_subscription",
			args: {
				subscription: frm.doc.name,
				status: status
			},
			callback: function(r) {
				if(r.message) {
					frm.set_value("status", r.message);
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
					frm.reload_doc();
				}
			}
		});
	}
<<<<<<< HEAD
});
=======
});
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
