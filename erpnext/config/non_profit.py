from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Chapter"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Chapter",
					"description": _("Chapter information."),
				}
			]
		},
		{
			"label": _("Membership"),
			"items": [
				{
					"type": "doctype",
					"name": "Member",
					"description": _("Member information."),
				},
				{
					"type": "doctype",
					"name": "Membership",
					"description": _("Memebership Details"),
				},
				{
					"type": "doctype",
					"name": "Membership Type",
					"description": _("Memebership Type Details"),
				},
			]
		},
		{
			"label": _("Volunteer"),
			"items": [
				{
					"type": "doctype",
					"name": "Volunteer",
					"description": _("Volunteer information."),
				},
				{
					"type": "doctype",
					"name": "Volunteer Type",
					"description": _("Volunteer Type information."),
				}
			]
		},
		{
			"label": _("Donor"),
			"items": [
				{
					"type": "doctype",
					"name": "Donor",
					"description": _("Donor information."),
				},
				{
					"type": "doctype",
					"name": "Donor Type",
					"description": _("Donor Type information."),
				}
			]
		},
		{
<<<<<<< HEAD
			"label": _("Loan Management"),
			"icon": "icon-list",
			"items": [
				{
					"type": "doctype",
					"name": "Loan Type",
					"description": _("Define various loan types")
				},
				{
					"type": "doctype",
					"name": "Loan Application",
					"description": _("Loan Application")
				},
				{
					"type": "doctype",
					"name": "Loan"
				},
			]
		},
		{
=======
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
			"label": _("Grant Application"),
			"items": [
				{
					"type": "doctype",
					"name": "Grant Application",
					"description": _("Grant information."),
				}
			]
		}
	]
