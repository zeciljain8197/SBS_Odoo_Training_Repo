

{
    'name': 'Formula1 Fan Management',
    'description': '''This modules is used to manage Formula 1 fans portal.''',
    'version': '1.0',
    'category': 'formula1',
    'depends': ['base', 'mail'],
    'author': 'Zecil Jain',
    'website': 'https://www.formula1.com/',
    'data': [
        'security/formula1_security.xml',
        'security/ir.model.access.csv',
        'data/constr_sequence.xml',
        'views/view_constr_view.xml',
        'views/update_fans_view.xml',
        'views/update_circuit_cost_view.xml',
        'views/update_entry_fees_view.xml',
        'views/update_driver_wins_view.xml',
        'views/update_driver_wins_inherit_view.xml',
        'views/constructor_xls_wiz_view.xml',
        'views/constructor_report_view.xml',
        'views/overall_report_view.xml',
        'views/overall_report_template.xml',
        'views/constructor_report_template.xml',
        'report/overall_reports.xml',
        'views/constructors_view.xml',
        'views/update_fans_alt_view.xml',
        'report/constructor_reports.xml',
        'report/constructor_analysis_report_view.xml',
    ],
    'assets': {
        'web.assets_backend': ['formula1/static/src/scss/formula1.scss'],
    },
    'installable': True,
    'auto_install': False,
    'application': True
}
