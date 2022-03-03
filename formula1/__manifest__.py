{
    'name': 'Formula1 Fan Management',
    'description': '''This modules is used to manage Formula 1 fans portal.''',
    'version': '1.0',
    'category': 'formula1',
    'depends': ['base'],
    'author': 'Zecil Jain',
    'website': 'https://www.formula1.com/',
    'data': [
        'security/formula1_security.xml',
        'security/ir.model.access.csv',
        'views/constructors_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}