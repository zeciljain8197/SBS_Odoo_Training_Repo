{
    'name': 'Academy Driver Management',
    'description': '''This modules is used to extend features of formula1 module''',
    'version': '1.0',
    'category': 'Formula1',
    'depends': ['formula1','mail'],
    'author': 'Zecil Jain',
    'website': 'https://www.formula1.com/',
    'data': [
        'security/ir.model.access.csv',
        'views/update_fan_visit_view.xml',
        'views/academy_view.xml',
        'views/multiple_view.xml',
        'views/template_view.xml',
        'report/constructor_analysis_report_view.xml',
        'views/constructor_report_template.xml',
        'views/overall_report_view.xml',
        'views/overall_report_template.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}