frappe.ui.form.on('Holiday List', {
    refresh: (frm) => {
        frm.set_query("holiday_type", () => {
            return {
                query: "holidays.utils.holiday_type_query",
                filters: {
                    country: frm.doc.country,
                    from_date: frm.doc.from_date,
                    to_date: frm.doc.to_date,
                },
            };
        });
    },
    add_country_holidays: (frm) => {
        const mandatory_fields = ['country', 'holiday_type', 'from_date', 'to_date'];
        mandatory_fields.map(fieldname => {
            if (!frm.doc[fieldname]) {
                frappe.throw(`Please select ${fieldname}`);
            }
        })
        
        frappe.call({
            method: "holidays.utils.get_holidays",
            type: "POST",
            args: {
                country: frm.doc.country,
                holiday_type: frm.doc.holiday_type,
                from_date: frm.doc.from_date,
                to_date: frm.doc.to_date,
            },
            callback: (r) => {
                if (r.exc) {
                    frappe.throw(r.exc);
                } else {
                    if (r.message && r.message.length > 0) {
                        r.message.map(row => {
                            frm.add_child('holidays', {
                                holiday_date: row.date,
                                description: row.description
                            });
                            frm.refresh_field('holidays');
                        })
                        frappe.msgprint(`Added ${r.message.length} holidays.`)
                    } else {
                        frappe.throw("No holidays found.");
                    }
                }
            },
            freeze: true,
            freeze_message: "Please wait...",
            async: true,
        });
    }
})