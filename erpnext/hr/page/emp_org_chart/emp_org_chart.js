frappe.pages['emp_org_chart'].on_page_load = function(wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Emp Org Chart'),
		single_column: true
	});

	wrapper.emp_org_chart = new erpnext.EmpOrgChart(wrapper);

	frappe.breadcrumbs.add("HR");
}

erpnext.EmpOrgChart = Class.extend({
	init: function(wrapper) {
		var me = this;
		// 0 setTimeout hack - this gives time for canvas to get width and height
		setTimeout(function() {
			me.setup(wrapper);
			me.get_parent_employees(me);
//			me.get_employee_data(me);
//			me.get_parent_children(me);
		}, 0);
	},
	
	get_parent_employees: function(frm) {
		var mail_html_str = '<div id="wrapper">'
		frappe.call({
			method: "erpnext.hr.page.emp_org_chart.emp_org_chart.get_parent_employees",
			callback: function(r) {
				console.log(":::::::MAIN:::::::::",r.message);
//				r.message.forEach(function(message, i) {
//					console.log(":::::::MY TEST:::::::::",message, i);
//					console.log(":::::::MY TEST:::::::::",message, i);
//				});
				if (r.message){
//					console.log(":::::::r.msg:::::::::",r.message);
					for (var key in r.message) {
						console.log(":::::::key111::::::::",key);
						console.log(":::::::key222::::::::",r.message[key]);
						
//							mail_html_str += '<ul>'
//								mail_html_str += '<li>'
//								mail_html_str += '<span> '+ key +' </span>'
//									mail_html_str += '<ul>'
//										mail_html_str += '<li>'
//										mail_html_str += '<span> '+ r.message[key][0] +' </span>'
//										mail_html_str += '</li>'
//										mail_html_str += '<li>'
//										mail_html_str += '<span> '+ r.message[key][1] +' </span>'
//										mail_html_str += '</li>'
//									mail_html_str += '</ul>'
//								mail_html_str += '</li>'
//								
//								mail_html_str += '<li>'
//									mail_html_str += '<span> '+ key +' </span>'
//										mail_html_str += '<ul>'
//											mail_html_str += '<li>'
//											mail_html_str += '<span> '+ r.message[key][0] +' </span>'
//											mail_html_str += '</li>'
//											mail_html_str += '<li>'
//											mail_html_str += '<span> '+ r.message[key][1] +' </span>'
//											mail_html_str += '</li>'
//										mail_html_str += '</ul>'
//								mail_html_str += '</li>'
//							mail_html_str += '</ul>'
						
						mail_html_str += '<ul class="tree">'
						mail_html_str += '<li>'
						mail_html_str += '<span>Root</span>'		
							
						mail_html_str += '<ul>'
						mail_html_str += '<li>'
						mail_html_str += '<span> '+ key +' </span>'
								mail_html_str += '<ul>'
									mail_html_str += '<li>'
									mail_html_str += '<span> '+ r.message[key][0] +' </span>'
									mail_html_str += '</li>'
									mail_html_str += '<li>'
									mail_html_str += '<span> '+ r.message[key][1] +' </span>'
									mail_html_str += '</li>'
								mail_html_str += '</ul>'
						mail_html_str += '</li>'
//							
//						mail_html_str += '<li>'
//						mail_html_str += '<span> '+ key +' </span>'
//									mail_html_str += '<ul>'
//										mail_html_str += '<li>'
//										mail_html_str += '<span> '+ r.message[key][0] +' </span>'
//										mail_html_str += '</li>'
//										mail_html_str += '<li>'
//										mail_html_str += '<span> '+ r.message[key][1] +' </span>'
//										mail_html_str += '</li>'
//									mail_html_str += '</ul>'
//						mail_html_str += '</li>'
						mail_html_str += '</ul>'		
								
						mail_html_str += '</li>'
						mail_html_str += '</ul>'
						mail_html_str += '</div>'
					

					}
					
					frm.elements.hr_wrapper.append(mail_html_str);
				}
			
			}
		});
	},
//	get_employee_data: function(frm) {
//		var mail_html_str = '<div class="pos">'
//			mail_html_str += '<section class="cart-container"></section>'
//			mail_html_str += '<section class="item-container">'
//			mail_html_str += '<div class="content">'
//			mail_html_str += '<h1>Employee Organization Chart</h1>'
//			mail_html_str += '<figure class="org-chart cf">'
//		frappe.call({
//			method: "erpnext.hr.page.emp_org_chart.emp_org_chart.get_employee_data",
//			callback: function(r) {
//
//				console.log(":::::get_employee_data:::::::",r.message[0].name);
//				mail_html_str += '<ul1>'
//				mail_html_str += '<li>'	
//				mail_html_str += '<ul class="director">'	
//				mail_html_str += '<li>'
//				mail_html_str += '<a href="#"><span>' + r.message[0].name +'</span></a>'
//				mail_html_str += '<ul class="subdirector">'
//				mail_html_str += '<li><a href="#"><span>' + r.message[0].name +'</span></a></li>'
//				mail_html_str += '</ul>'
//				mail_html_str += '<ul class="departments cf">'
//				mail_html_str += '<li><a href="#"><span>' + r.message[0].name +'</span></a></li>'
//				mail_html_str += '<li class="department dep-a">'
//				mail_html_str += '<a href="#"><span>' + r.message[0].name +'</span></a>'
//				mail_html_str += '<ul class="sections">'
//				mail_html_str += '<li class="section"><a href="#"><span>' + r.message[0].name +'</span></a></li>'
//				mail_html_str += '<li class="section"><a href="#"><span>' + r.message[0].name +'</span></a></li>'
//				mail_html_str += '<li class="section"><a href="#"><span>' + r.message[0].name +'</span></a></li>'
//				mail_html_str += '<li class="section"><a href="#"><span>' + r.message[0].name +'</span></a></li>'
//				mail_html_str += '<li class="section"><a href="#"><span>' + r.message[0].name +'</span></a></li>'
//				mail_html_str += '</ul>'
//				mail_html_str += '</li>'
//
//				mail_html_str += '</ul>'
//				mail_html_str += '</li>'
//				mail_html_str += '</ul>'
//				mail_html_str += '</li>'
//				mail_html_str += '</ul1>'
//				mail_html_str += '</figure>'
//				mail_html_str += '</div>'
//				mail_html_str += '</section>'
//				mail_html_str += '</div>'
//				
//				frm.elements.hr_wrapper.append(mail_html_str);
//			},
//		});
//	},
	
	setup: function(wrapper) {
		var me = this;

		this.elements = {
			layout: $(wrapper).find(".layout-main"),
//			company: wrapper.page.add_date(__("Company")),
			refresh_btn: wrapper.page.set_primary_action(__("Refresh"),
				function() { }, "fa fa-refresh"),
		};
	
//		this.elements.no_data = $('<div class="alert alert-warning">' + __("No Data") + '</div>')
//			.toggle(false)
//			.appendTo(this.elements.layout);
		
		this.elements.hr_wrapper = $('<div class="hr-wrapper text-center"> </div>')
			.appendTo(this.elements.layout);
	},
});

