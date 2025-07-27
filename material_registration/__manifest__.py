{
    'name': 'Material Registration',
    'version': '14.0.1.0.0',
    'summary': 'Module for Material Registration',
    'category': 'Inventory',
    'author': '',
    'maintainer': '',
    'website': '-',
    'license': 'LGPL-3',
    'description': """
        * 2025-07-26
            - Add new model Material Registration
            - Manage material registration product
            - Add filter on Material Registration
    """,
    'contributors': [
        'Fitrohudin <fitrohudinmuhammad@gmail.com>',
    ],
    'depends': [
        'base',
        'stock',
        'sale',
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        
        'views/material_registration_views.xml',
        
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
