// Copyright (c) 2025, demo_app and contributors
// For license information, please see license.txt


frappe.ui.form.on("Client Side Scripting", {
    
	// refresh(frm) {
        // // frappe.msgprint("Hello")
        // frappe.throw("THIS IS AN ERROR")

        // onload(frm){
        //         frappe.msgprint("hii")
        // }

//     refresh: function(frm) {
//         frm.add_custom_button("Say Hello", function() {
//             frappe.msgprint("Hello from client script!");
//         });
//     }
// });



// --->value fetching

    // before_save:function(frm){
    //     frappe.msgprint("The full name is '{0}'",
    //         [frm.doc.first_name + " "+frm.doc.middle_name +" "+frm.doc.last_name]
    //     )
    // }
    
    // first_name: function(frm) {--> not done
    //     frappe.db.get_value("Client Side Scripting", { first_name: frm.doc.first_name }, "last_name")
    //         .then(r => {
    //             if (r.message) {
    //                 frappe.msgprint("Fetched Last Name: " + r.message.last_name);
    //             } else {
    //                 frappe.msgprint("No record found!");
    //             }
    //         });
    // }



    

    // -->set_intro
    // refresh:function(frm){
    //     frm.set_intro("this is intro event")
    // }


    // -->set_value

    // validate:function(frm){
    //     frm.set_value('full_name',frm.doc.first_name +" "+frm.doc.middle_name +" "+frm.doc.last_name)
    

    // refresh:function(frm){
    //     frm.set_value('first_name','raghav')
    // }
//    -->add_child 
    // let row=frm.add_child('family_members',{
    //     name1:'smith',
    //     relation:'father',
    //     age:52,
    // })
// }


// -->set_df_property

    // enable:function(frm){
    //     frm.set_df_property("email","reqd",1)

    //     frm.set_df_property('middle_name','read_only',1)

    //     // frm.toggle_reqd('age',true)
    // }


    // -->add_custom_button

    refresh:function(frm){
        frm.add_custom_button('New Button',() =>{
            frappe.msgprint("Hello from Custom Button")
        })
    }
     




    // -->value fetching prac
	// refresh:function(frm){
    //     let f =frm.doc.first_name;
    //     frappe.msgprint("First Name is:"+f);
    // }

    // })
   
    
    
//     refresh: function(frm) {
//         frappe.db.get_value("Client Side Scripting", { name: frm.doc.first_name }, "first_name")
//             .then(r => {
//                 if (r.message) {
//                     frappe.msgprint("Fetched Name: " + r.message.first_name);
//                 }
//             });
//     }
});


