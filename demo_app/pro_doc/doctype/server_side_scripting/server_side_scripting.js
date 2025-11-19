// Copyright (c) 2025, demo_app and contributors
// For license information, please see license.txt


frappe.ui.form.on("Server Side Scripting", {
	enable:function(frm) {
        console.log("------------------",frm.doc)
        frappe.call({
            // doc:frm.doc,
            method:'demo_app.pro_doc.doctype.client_side_scripting.client_side_scripting.frappe_call',
            args:{
                msg:'Hello'
            },
            freeze: true,
            freeze_message : ('Calling frappe_call method'),
            callback: function(r){
                console.log('r -----------------', r)
                frappe.msgprint(r.message)
            }
        });

	}
});










// frappe.ui.form.on("Server Side Scripting", {
// 	enable:function(frm) {
//         frm.call({
//             doc:frm.doc,
//             method:'frm_call',
//             args:{
//                 msg:'Hello'
//             },
//             freeze: true,
//             freeze_message : ('Calling frm_call method'),
//             callback: function(r){
//                 // frappe.msgprint(r.message)
//             }
//         });

// 	}
// });
