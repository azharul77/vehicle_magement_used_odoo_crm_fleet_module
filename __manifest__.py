# -*- coding: utf-8 -*-
{
    'name': 'Vehicle repair and maintenance service management software',
    'summary': """This is a management software""",
    'description': """
App Name
========
Something about the App.
    """,
    'version': '13.0.1.0',
    'author': 'A.T.M Shamiul Bashir',
    'website': 'http://shamiulbashir.github.io',
    'category': 'Tools',
    'sequence': 1,
    'depends': [
        'base',
        'account',
        'web',
        'mail',
        'crm',
        'fleet',
    ],
    'data': [

        ## Security
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',

        ## Report
        # 'reports/report_paper_format.xml',
        # 'reports/my_model_name_report.xml',
        
        ## View & Wizard
        'views/vehicle_info.xml',
        'views/services.xml',
        'views/vehicle_brand.xml',
        'views/vehicle_repair.xml',

    ],
    'qweb': [],
    'demo': [],
    'external_dependencies': {
        'python': [
            'werkzeug',
        ],
    },
    'icon': '/vehicle_managment_system/static/description/car.png',
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 0,
    'currency': 'EUR',
    'license': 'OPL-1',
    'contributors': [
        'Azharul Amin Mulla',
    ],
        
}
