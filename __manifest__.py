{
    'name': 'Execute Python & PSQL From UI',
    'summary': """Execute Python, Execute PostgreSQL From The Odoo 17 UI""",
    'description': 'Execute Python and Postgres from the UI under Settings > Technical',
    'version': '17.0.1.0.1',
    'depends': ['base', 'mail'],
    'author': 'onev1rod',
    'category': '',
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/execute_python_views.xml',
        'views/execute_postgres_views.xml',
        'views/execute_menu.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'images': [],
    'application': 'True',
    'installable': 'True',
    'license': 'LGPL-3',
    'assets': {},
}
