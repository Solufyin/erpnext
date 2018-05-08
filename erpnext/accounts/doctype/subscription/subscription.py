# -*- coding: utf-8 -*-
<<<<<<< HEAD
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import nowdate, getdate, cint, add_days, date_diff, get_last_day, add_to_date, flt


class Subscription(Document):
	def before_insert(self):
		# update start just before the subscription doc is created
		self.update_subscription_period(self.start)

	def update_subscription_period(self, date=None):
		"""
		Subscription period is the period to be billed. This method updates the
		beginning of the billing period and end of the billing period.

		The beginning of the billing period is represented in the doctype as
		`current_invoice_start` and the end of the billing period is represented
		as `current_invoice_end`.
		"""
		self.set_current_invoice_start(date)
		self.set_current_invoice_end()

	def set_current_invoice_start(self, date=None):
		"""
		This sets the date of the beginning of the current billing period.
		If the `date` parameter is not given , it will be automatically set as today's
		date.
		"""
		if self.trial_period_start and self.is_trialling():
			self.current_invoice_start = self.trial_period_start
		elif not date:
			self.current_invoice_start = nowdate()
		elif date:
			self.current_invoice_start = date

	def set_current_invoice_end(self):
		"""
		This sets the date of the end of the current billing period.

		If the subscription is in trial period, it will be set as the end of the
		trial period.

		If is not in a trial period, it will be `x` days from the beginning of the
		current billing period where `x` is the billing interval from the
		`Subscription Plan` in the `Subscription`.
		"""
		if self.is_trialling():
			self.current_invoice_end = self.trial_period_end
		else:
			billing_cycle_info = self.get_billing_cycle()
			if billing_cycle_info:
				self.current_invoice_end = add_to_date(self.current_invoice_start, **billing_cycle_info)
			else:
				self.current_invoice_end = get_last_day(self.current_invoice_start)

	def get_billing_cycle(self):
		"""
		Returns a dict containing billing cycle information deduced from the
		`Subscription Plan` in the `Subscription`.
		"""
		return self.get_billing_cycle_data()

	@staticmethod
	def validate_plans_billing_cycle(billing_cycle_data):
		"""
		Makes sure that all `Subscription Plan` in the `Subscription` have the
		same billing interval
		"""
		if billing_cycle_data and len(billing_cycle_data) != 1:
			frappe.throw(_('You can only have Plans with the same billing cycle in a Subscription'))

	def get_billing_cycle_and_interval(self):
		"""
		Returns a dict representing the billing interval and cycle for this `Subscription`.

		You shouldn't need to call this directly. Use `get_billing_cycle` instead.
		"""
		plan_names = [plan.plan for plan in self.plans]
		billing_info = frappe.db.sql(
			'select distinct `billing_interval`, `billing_interval_count` '
			'from `tabSubscription Plan` '
			'where name in %s',
			(plan_names,), as_dict=1
		)

		return billing_info

	def get_billing_cycle_data(self):
		"""
		Returns dict contain the billing cycle data.

		You shouldn't need to call this directly. Use `get_billing_cycle` instead.
		"""
		billing_info = self.get_billing_cycle_and_interval()

		self.validate_plans_billing_cycle(billing_info)

		if billing_info:
			data = dict()
			interval = billing_info[0]['billing_interval']
			interval_count = billing_info[0]['billing_interval_count']
			if interval not in ['Day', 'Week']:
				data['days'] = -1
			if interval == 'Day':
				data['days'] = interval_count - 1
			elif interval == 'Month':
				data['months'] = interval_count
			elif interval == 'Year':
				data['years'] = interval_count
			# todo: test week
			elif interval == 'Week':
				data['days'] = interval_count * 7 - 1

			return data

	def set_status_grace_period(self):
		"""
		Sets the `Subscription` `status` based on the preference set in `Subscription Settings`.

		Used when the `Subscription` needs to decide what to do after the current generated
		invoice is past it's due date and grace period.
		"""
		subscription_settings = frappe.get_single('Subscription Settings')
		if self.status == 'Past Due Date' and self.is_past_grace_period():
			self.status = 'Cancelled' if cint(subscription_settings.cancel_after_grace) else 'Unpaid'

	def set_subscription_status(self):
		"""
		Sets the status of the `Subscription`
		"""
		if self.is_trialling():
			self.status = 'Trialling'
		elif self.status == 'Past Due Date' and self.is_past_grace_period():
			subscription_settings = frappe.get_single('Subscription Settings')
			self.status = 'Cancelled' if cint(subscription_settings.cancel_after_grace) else 'Unpaid'
		elif self.status == 'Past Due Date' and not self.has_outstanding_invoice():
			self.status = 'Active'
		elif self.current_invoice_is_past_due():
			self.status = 'Past Due Date'
		elif self.is_new_subscription():
			self.status = 'Active'
			# todo: then generate new invoice
		self.save()

	def is_trialling(self):
		"""
		Returns `True` if the `Subscription` is trial period.
		"""
		return not self.period_has_passed(self.trial_period_end) and self.is_new_subscription()

	@staticmethod
	def period_has_passed(end_date):
		"""
		Returns true if the given `end_date` has passed
		"""
		# todo: test for illegal time
		if not end_date:
			return True

		end_date = getdate(end_date)
		return getdate(nowdate()) > getdate(end_date)

	def is_past_grace_period(self):
		"""
		Returns `True` if the grace period for the `Subscription` has passed
		"""
		current_invoice = self.get_current_invoice()
		if self.current_invoice_is_past_due(current_invoice):
			subscription_settings = frappe.get_single('Subscription Settings')
			grace_period = cint(subscription_settings.grace_period)

			return getdate(nowdate()) > add_days(current_invoice.due_date, grace_period)

	def current_invoice_is_past_due(self, current_invoice=None):
		"""
		Returns `True` if the current generated invoice is overdue
		"""
		if not current_invoice:
			current_invoice = self.get_current_invoice()

		if not current_invoice:
			return False
		else:
			return getdate(nowdate()) > getdate(current_invoice.due_date)

	def get_current_invoice(self):
		"""
		Returns the most recent generated invoice.
		"""
		if len(self.invoices):
			current = self.invoices[-1]
			if frappe.db.exists('Sales Invoice', current.invoice):
				doc = frappe.get_doc('Sales Invoice', current.invoice)
				return doc
			else:
				frappe.throw(_('Invoice {0} no longer exists'.format(current.invoice)))

	def is_new_subscription(self):
		"""
		Returns `True` if `Subscription` has never generated an invoice
		"""
		return len(self.invoices) == 0

	def validate(self):
		self.validate_trial_period()
		self.validate_plans_billing_cycle(self.get_billing_cycle_and_interval())

	def validate_trial_period(self):
		"""
		Runs sanity checks on trial period dates for the `Subscription`
		"""
		if self.trial_period_start and self.trial_period_end:
			if getdate(self.trial_period_end) < getdate(self.trial_period_start):
				frappe.throw(_('Trial Period End Date Cannot be before Trial Period Start Date'))

		elif self.trial_period_start or self.trial_period_end:
			frappe.throw(_('Both Trial Period Start Date and Trial Period End Date must be set'))

	def after_insert(self):
		# todo: deal with users who collect prepayments. Maybe a new Subscription Invoice doctype?
		self.set_subscription_status()

	def generate_invoice(self, prorate=0):
		"""
		Creates a `Sales Invoice` for the `Subscription`, updates `self.invoices` and
		saves the `Subscription`.
		"""
		invoice = self.create_invoice(prorate)
		self.append('invoices', {'invoice': invoice.name})
		self.save()

		return invoice

	def create_invoice(self, prorate):
		"""
		Creates a `Sales Invoice`, submits it and returns it
		"""
		invoice = frappe.new_doc('Sales Invoice')
		invoice.set_posting_time = 1
		invoice.posting_date = self.current_invoice_start
		invoice.customer = self.get_customer(self.subscriber)

		# Subscription is better suited for service items. I won't update `update_stock`
		# for that reason
		items_list = self.get_items_from_plans(self.plans, prorate)
		for item in items_list:
			item['qty'] = self.quantity
			invoice.append('items',	item)

		# Taxes
		if self.tax_template:
			invoice.taxes_and_charges = self.tax_template
			invoice.set_taxes()

		# Due date
		invoice.append(
			'payment_schedule',
			{
				'due_date': add_days(self.current_invoice_end, cint(self.days_until_due)),
				'invoice_portion': 100
			}
		)

		# Discounts
		if self.additional_discount_percentage:
			invoice.additional_discount_percentage = self.additional_discount_percentage

		if self.additional_discount_amount:
			invoice.discount_amount = self.additional_discount_amount

		if self.additional_discount_percentage or self.additional_discount_amount:
			discount_on = self.apply_additional_discount
			invoice.apply_additional_discount = discount_on if discount_on else 'Grand Total'

		invoice.flags.ignore_mandatory = True
		invoice.save()
		invoice.submit()

		return invoice

	@staticmethod
	def get_customer(subscriber_name):
		"""
		Returns the `Customer` linked to the `Subscriber`
		"""
		return frappe.get_value('Subscriber', subscriber_name)

	def get_items_from_plans(self, plans, prorate=0):
		"""
		Returns the `Item`s linked to `Subscription Plan`
		"""
		plan_items = [plan.plan for plan in plans]
		item_names = None

		if plan_items and not prorate:
			item_names = frappe.db.sql(
				'select item as item_code, cost as rate from `tabSubscription Plan` where name in %s',
				(plan_items,), as_dict=1
			)

		elif plan_items:
			prorate_factor = get_prorata_factor(self.current_invoice_end, self.current_invoice_start)

			item_names = frappe.db.sql(
				'select item as item_code, cost * %s as rate from `tabSubscription Plan` where name in %s',
				(prorate_factor, plan_items,), as_dict=1
			)

		return item_names

	def process(self):
		"""
		To be called by task periodically. It checks the subscription and takes appropriate action
		as need be. It calls either of these methods depending the `Subscription` status:
		1. `process_for_active`
		2. `process_for_past_due`
		"""
		if self.status == 'Active':
			self.process_for_active()
		elif self.status in ['Past Due Date', 'Unpaid']:
			self.process_for_past_due_date()

		self.save()

	def process_for_active(self):
		"""
		Called by `process` if the status of the `Subscription` is 'Active'.

		The possible outcomes of this method are:
		1. Generate a new invoice
		2. Change the `Subscription` status to 'Past Due Date'
		3. Change the `Subscription` status to 'Cancelled'
		"""
		if getdate(nowdate()) > getdate(self.current_invoice_end) and not self.has_outstanding_invoice():
			self.generate_invoice()
			if self.current_invoice_is_past_due():
				self.status = 'Past Due Date'

		if self.current_invoice_is_past_due() and getdate(nowdate()) > getdate(self.current_invoice_end):
			self.status = 'Past Due Date'

		if self.cancel_at_period_end and getdate(nowdate()) > self.current_invoice_end:
			self.cancel_subscription_at_period_end()

	def cancel_subscription_at_period_end(self):
		"""
		Called when `Subscription.cancel_at_period_end` is truthy
		"""
		self.status = 'Cancelled'
		if not self.cancelation_date:
			self.cancelation_date = nowdate()

	def process_for_past_due_date(self):
		"""
		Called by `process` if the status of the `Subscription` is 'Past Due Date'.

		The possible outcomes of this method are:
		1. Change the `Subscription` status to 'Active'
		2. Change the `Subscription` status to 'Cancelled'
		3. Change the `Subscription` status to 'Unpaid'
		"""
		current_invoice = self.get_current_invoice()
		if not current_invoice:
			frappe.throw(_('Current invoice {0} is missing'.format(current_invoice.invoice)))
		else:
			if self.is_not_outstanding(current_invoice):
				self.status = 'Active'
				self.update_subscription_period(nowdate())
			else:
				self.set_status_grace_period()

	@staticmethod
	def is_not_outstanding(invoice):
		"""
		Return `True` if the given invoice is paid
		"""
		return invoice.status == 'Paid'

	def has_outstanding_invoice(self):
		"""
		Returns `True` if the most recent invoice for the `Subscription` is not paid
		"""
		current_invoice = self.get_current_invoice()
		if not current_invoice:
			return False
		else:
			return not self.is_not_outstanding(current_invoice)

	def cancel_subscription(self):
		"""
		This sets the subscription as cancelled. It will stop invoices from being generated
		but it will not affect already created invoices.
		"""
		if self.status != 'Cancelled':
			to_generate_invoice = True if self.status == 'Active' else False
			to_prorate = frappe.db.get_single_value('Subscription Settings', 'prorate')
			self.status = 'Cancelled'
			self.cancelation_date = nowdate()
			if to_generate_invoice:
				self.generate_invoice(prorate=to_prorate)
			self.save()

	def restart_subscription(self):
		"""
		This sets the subscription as active. The subscription will be made to be like a new
		subscription and the `Subscription` will lose all the history of generated invoices
		it has.
		"""
		if self.status == 'Cancelled':
			self.status = 'Active'
			self.db_set('start', nowdate())
			self.update_subscription_period(nowdate())
			self.invoices = []
			self.save()
		else:
			frappe.throw(_('You cannot restart a Subscription that is not cancelled.'))

	def get_precision(self):
		invoice = self.get_current_invoice()
		if invoice:
			return invoice.precision('grand_total')


def get_prorata_factor(period_end, period_start):
	diff = flt(date_diff(nowdate(), period_start) + 1)
	plan_days = flt(date_diff(period_end, period_start) + 1)
	prorate_factor = diff / plan_days

	return prorate_factor


def process_all():
	"""
	Task to updates the status of all `Subscription` apart from those that are cancelled
	"""
	subscriptions = get_all_subscriptions()
	for subscription in subscriptions:
		process(subscription)


def get_all_subscriptions():
	"""
	Returns all `Subscription` documents
	"""
	return frappe.db.sql(
		'select name from `tabSubscription` where status != "Cancelled"',
		as_dict=1
	)


def process(data):
	"""
	Checks a `Subscription` and updates it status as necessary
	"""
	if data:
		try:
			subscription = frappe.get_doc('Subscription', data['name'])
			subscription.process()
			frappe.db.commit()
		except frappe.ValidationError:
			frappe.db.rollback()
			frappe.db.begin()
			frappe.log_error(frappe.get_traceback())
			frappe.db.commit()


@frappe.whitelist()
def cancel_subscription(name):
	"""
	Cancels a `Subscription`. This will stop the `Subscription` from further invoicing the
	`Subscriber` but all already outstanding invoices will not be affected.
	"""
	subscription = frappe.get_doc('Subscription', name)
	subscription.cancel_subscription()


@frappe.whitelist()
def restart_subscription(name):
	"""
	Restarts a cancelled `Subscription`. The `Subscription` will 'forget' the history of
	all invoices it has generated
	"""
	subscription = frappe.get_doc('Subscription', name)
	subscription.restart_subscription()


@frappe.whitelist()
def get_subscription_updates(name):
	"""
	Use this to get the latest state of the given `Subscription`
	"""
	subscription = frappe.get_doc('Subscription', name)
	subscription.process()
=======
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import calendar
from frappe import _
from frappe.desk.form import assign_to
from frappe.utils.jinja import validate_template
from dateutil.relativedelta import relativedelta
from frappe.utils.user import get_system_managers
from frappe.utils import cstr, getdate, split_emails, add_days, today, get_last_day, get_first_day
from frappe.model.document import Document

month_map = {'Monthly': 1, 'Quarterly': 3, 'Half-yearly': 6, 'Yearly': 12}
class Subscription(Document):
	def validate(self):
		self.update_status()
		self.validate_reference_doctype()
		self.validate_dates()
		self.validate_next_schedule_date()
		self.validate_email_id()

		validate_template(self.subject or "")
		validate_template(self.message or "")

	def before_submit(self):
		if not self.next_schedule_date:
			self.next_schedule_date = get_next_schedule_date(self.start_date,
				self.frequency, self.repeat_on_day)

	def on_submit(self):
		self.update_subscription_id()

	def on_update_after_submit(self):
		self.validate_dates()
		self.set_next_schedule_date()

	def before_cancel(self):
		self.unlink_subscription_id()
		self.next_schedule_date = None

	def unlink_subscription_id(self):
		frappe.db.sql("update `tab{0}` set subscription = null where subscription=%s"
			.format(self.reference_doctype), self.name)

	def validate_reference_doctype(self):
		if not frappe.get_meta(self.reference_doctype).has_field('subscription'):
			frappe.throw(_("Add custom field Subscription in the doctype {0}").format(self.reference_doctype))

	def validate_dates(self):
		if self.end_date and getdate(self.start_date) > getdate(self.end_date):
			frappe.throw(_("End date must be greater than start date"))

	def validate_next_schedule_date(self):
		if self.repeat_on_day and self.next_schedule_date:
			next_date = getdate(self.next_schedule_date)
			if next_date.day != self.repeat_on_day:
				# if the repeat day is the last day of the month (31)
				# and the current month does not have as many days,
				# then the last day of the current month is a valid date
				lastday = calendar.monthrange(next_date.year, next_date.month)[1]
				if self.repeat_on_day < lastday:

					# the specified day of the month is not same as the day specified
					# or the last day of the month
					frappe.throw(_("Next Date's day and Repeat on Day of Month must be equal"))

	def validate_email_id(self):
		if self.notify_by_email:
			if self.recipients:
				email_list = split_emails(self.recipients.replace("\n", ""))

				from frappe.utils import validate_email_add
				for email in email_list:
					if not validate_email_add(email):
						frappe.throw(_("{0} is an invalid email address in 'Recipients'").format(email))
			else:
				frappe.throw(_("'Recipients' not specified"))

	def set_next_schedule_date(self):
		if self.repeat_on_day:
			self.next_schedule_date = get_next_date(self.next_schedule_date, 0, self.repeat_on_day)

	def update_subscription_id(self):
		frappe.db.set_value(self.reference_doctype, self.reference_document, "subscription", self.name)

	def update_status(self, status=None):
		self.status = {
			'0': 'Draft',
			'1': 'Submitted',
			'2': 'Cancelled'
		}[cstr(self.docstatus or 0)]

		if status and status != 'Resumed':
			self.status = status

def get_next_schedule_date(start_date, frequency, repeat_on_day):
	mcount = month_map.get(frequency)
	if mcount:
		next_date = get_next_date(start_date, mcount, repeat_on_day)
	else:
		days = 7 if frequency == 'Weekly' else 1
		next_date = add_days(start_date, days)
	return next_date

def make_subscription_entry(date=None):
	date = date or today()
	for data in get_subscription_entries(date):
		schedule_date = getdate(data.next_schedule_date)
		while schedule_date <= getdate(today()):
			create_documents(data, schedule_date)
			schedule_date = get_next_schedule_date(schedule_date,
				data.frequency, data.repeat_on_day)

			if schedule_date and not frappe.db.get_value('Subscription', data.name, 'disabled'):
				frappe.db.set_value('Subscription', data.name, 'next_schedule_date', schedule_date)

def get_subscription_entries(date):
	return frappe.db.sql(""" select * from `tabSubscription`
		where docstatus = 1 and next_schedule_date <=%s
			and reference_document is not null and reference_document != ''
			and next_schedule_date <= ifnull(end_date, '2199-12-31')
			and ifnull(disabled, 0) = 0 and status != 'Stopped' """, (date), as_dict=1)

def create_documents(data, schedule_date):
	try:
		doc = make_new_document(data, schedule_date)
		if data.notify_by_email and data.recipients:
			print_format = data.print_format or "Standard"
			send_notification(doc, data, print_format=print_format)

		frappe.db.commit()
	except Exception:
		frappe.db.rollback()
		frappe.db.begin()
		frappe.log_error(frappe.get_traceback())
		disable_subscription(data)
		frappe.db.commit()
		if data.reference_document and not frappe.flags.in_test:
			notify_error_to_user(data)

def disable_subscription(data):
	subscription = frappe.get_doc('Subscription', data.name)
	subscription.db_set('disabled', 1)

def notify_error_to_user(data):
	party = ''
	party_type = ''

	if data.reference_doctype in ['Sales Order', 'Sales Invoice', 'Delivery Note']:
		party_type = 'customer'
	elif data.reference_doctype in ['Purchase Order', 'Purchase Invoice', 'Purchase Receipt']:
		party_type = 'supplier'

	if party_type:
		party = frappe.db.get_value(data.reference_doctype, data.reference_document, party_type)

	notify_errors(data.reference_document, data.reference_doctype, party, data.owner, data.name)

def make_new_document(args, schedule_date):
	doc = frappe.get_doc(args.reference_doctype, args.reference_document)
	new_doc = frappe.copy_doc(doc, ignore_no_copy=False)
	update_doc(new_doc, doc , args, schedule_date)
	new_doc.insert(ignore_permissions=True)

	if args.submit_on_creation:
		new_doc.submit()

	return new_doc

def update_doc(new_document, reference_doc, args, schedule_date):
	new_document.docstatus = 0
	if new_document.meta.get_field('set_posting_time'):
		new_document.set('set_posting_time', 1)

	mcount = month_map.get(args.frequency)

	if new_document.meta.get_field('subscription'):
		new_document.set('subscription', args.name)

	for fieldname in ['naming_series', 'ignore_pricing_rule', 'posting_time'
		'select_print_heading', 'remarks', 'owner']:
		if new_document.meta.get_field(fieldname):
			new_document.set(fieldname, reference_doc.get(fieldname))

	# copy item fields
	if new_document.meta.get_field('items'):
		for i, item in enumerate(new_document.items):
			for fieldname in ("page_break",):
				item.set(fieldname, reference_doc.items[i].get(fieldname))

	for data in new_document.meta.fields:
		if data.fieldtype == 'Date' and data.reqd:
			new_document.set(data.fieldname, schedule_date)

	set_subscription_period(args, mcount, new_document)

	new_document.run_method("on_recurring", reference_doc=reference_doc, subscription_doc=args)

def set_subscription_period(args, mcount, new_document):
	if mcount and new_document.meta.get_field('from_date') and new_document.meta.get_field('to_date'):
		last_ref_doc = frappe.db.sql("""
			select name, from_date, to_date
			from `tab{0}`
			where subscription=%s and docstatus < 2
			order by creation desc
			limit 1
		""".format(args.reference_doctype), args.name, as_dict=1)

		if not last_ref_doc:
			return

		from_date = get_next_date(last_ref_doc[0].from_date, mcount)

		if (cstr(get_first_day(last_ref_doc[0].from_date)) == cstr(last_ref_doc[0].from_date)) and \
			(cstr(get_last_day(last_ref_doc[0].to_date)) == cstr(last_ref_doc[0].to_date)):
				to_date = get_last_day(get_next_date(last_ref_doc[0].to_date, mcount))
		else:
			to_date = get_next_date(last_ref_doc[0].to_date, mcount)

		new_document.set('from_date', from_date)
		new_document.set('to_date', to_date)

def get_next_date(dt, mcount, day=None):
	dt = getdate(dt)
	dt += relativedelta(months=mcount, day=day)

	return dt

def send_notification(new_rv, subscription_doc, print_format='Standard'):
	"""Notify concerned persons about recurring document generation"""
	print_format = print_format
	subject = subscription_doc.subject or ''
	message = subscription_doc.message or ''

	if not subscription_doc.subject:
		subject = _("New {0}: #{1}").format(new_rv.doctype, new_rv.name)
	elif "{" in subscription_doc.subject:
		subject = frappe.render_template(subscription_doc.subject, {'doc': new_rv})

	if not subscription_doc.message:
		message = _("Please find attached {0} #{1}").format(new_rv.doctype, new_rv.name)
	elif "{" in subscription_doc.message:
		message = frappe.render_template(subscription_doc.message, {'doc': new_rv})

	attachments = [frappe.attach_print(new_rv.doctype, new_rv.name,
		file_name=new_rv.name, print_format=print_format)]

	frappe.sendmail(subscription_doc.recipients,
		subject=subject, message=message, attachments=attachments)

def notify_errors(doc, doctype, party, owner, name):
	recipients = get_system_managers(only_name=True)
	frappe.sendmail(recipients + [frappe.db.get_value("User", owner, "email")],
		subject=_("[Urgent] Error while creating recurring %s for %s" % (doctype, doc)),
		message = frappe.get_template("templates/emails/recurring_document_failed.html").render({
			"type": _(doctype),
			"name": doc,
			"party": party or "",
			"subscription": name
		}))

	assign_task_to_owner(name, "Recurring Documents Failed", recipients)

def assign_task_to_owner(name, msg, users):
	for d in users:
		args = {
			'doctype'		:	'Subscription',
			'assign_to' 	:	d,
			'name'			:	name,
			'description'	:	msg,
			'priority'		:	'High'
		}
		assign_to.add(args)

@frappe.whitelist()
def make_subscription(doctype, docname):
	doc = frappe.new_doc('Subscription')

	reference_doc = frappe.get_doc(doctype, docname)
	doc.reference_doctype = doctype
	doc.reference_document = docname
	doc.start_date = reference_doc.get('posting_date') or reference_doc.get('transaction_date')
	return doc

@frappe.whitelist()
def stop_resume_subscription(subscription, status):
	doc = frappe.get_doc('Subscription', subscription)
	frappe.msgprint(_("Subscription has been {0}").format(status))
	if status == 'Resumed':
		doc.next_schedule_date = get_next_schedule_date(today(),
			doc.frequency, doc.repeat_on_day)

	doc.update_status(status)
	doc.save()

	return doc.status

def subscription_doctype_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select parent from `tabDocField`
		where fieldname = 'subscription'
			and parent like %(txt)s
		order by
			if(locate(%(_txt)s, parent), locate(%(_txt)s, parent), 99999),
			parent
		limit %(start)s, %(page_len)s""".format(**{
			'key': searchfield,
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		})
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
