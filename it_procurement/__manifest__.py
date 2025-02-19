{
    'name': 'IT Procurement',
    'version': '16.0.1.0.0',
    'category': 'Inventory/Purchase',
    'summary': 'IT Equipment Procurement Management',
    'description': """
        Manage IT equipment procurement process with approval workflow:
        * Create and track IT equipment purchase requests
        * Multi-level approval process (COO and MD)
        * Vendor notification system
        * Price-based approval routing
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'purchase',
        'website',
        'mail',
        'portal',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/purchase_order_views.xml',
        'views/report_template.xml',
        'views/website_templates.xml',
        'reports/purchase_order_report.py',
    ],
    'assets': {
        'web.assets_frontend': [
            'it_procurement/static/src/css/styles.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
} 