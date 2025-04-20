
{
    'name': "HMS",
    'summary': "Hospital Management System",
    'version': '1.0',
    'depends': ['base','mail','contacts'],
    'data': [
        'views/customer_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/hms_menus.xml',  
        'views/patient_status_report.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        
    ],
    'application': True,
    'installable': True,
}

