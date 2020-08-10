# -*- coding: utf-8 -*-

{
    'name': 'Visits Management',
    'version': '1.0',
    'sequence': 125,
    'description': """
        Track and Manage Visit Process""",
    'depends': ['custom_contract'],
    'summary': 'Track and Manage Visit Process',
    'website': 'https://www.odoo.com/page/tpm-maintenance-software',
    'data': [
        'security/visit_group.xml',
        'security/ir.model.access.csv',
        'data/visit_sequence.xml',
        'data/ir_cron.xml',
        'views/visit.xml',
        'views/maintenance.xml',
        'views/complaints.xml',
        'wizards/scheduling_visit_wizard_view.xml',
        'wizards/raise_complaints_wiz_view.xml',
        'views/extend_maintenance_contract.xml',
        # 'reports/maintenance_contract_template.xml',
    ],
    'installable': True,
    'application': True,
}
