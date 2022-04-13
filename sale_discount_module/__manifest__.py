{
    'name': 'Sale Discount Amount',
    'description': """This module is the extension of Sales module""",
    'version': '1.0',
    'category': 'Sales',
    'depends': ['sale'],
    'author': 'Zecil Jain',
    'data': [
        'views/account_view.xml',
        'views/discount_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
