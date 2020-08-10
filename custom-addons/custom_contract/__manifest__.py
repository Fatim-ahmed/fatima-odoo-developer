# -*- coding: utf-8 -*-

{
    'name': 'Contract',
    'version': '1.0',
    'sequence': 125,
    'description': """
        Track and Manage Contract""",
    'depends': ['sale_management'],
    'summary': 'Track and Manage Contract',
    'website': 'https://www.odoo.com/page/tpm-maintenance-software',
    'data': [
        'security/contract.xml',
        'security/ir.model.access.csv',
        'data/contract_sequence.xml',
        'demo/type_demo.xml',
        'views/contract.xml',
        'views/maintenance_contract.xml',
        'views/extend_res_partner_view.xml',
        'reports/agreement_contract_template.xml',
        'reports/maintenance_contract_template.xml',
    ],
    'installable': True,
    'application': True,
}
