# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ContractMaintenance(models.Model):
    _inherit = 'contract.maintenance'

    def action_scheduling_visit_contract(self):
        domain = []
        context = {}
        context = dict(self.env.context or {})
        context['default_contract_id'] = self.id
        context['default_first_visit_date'] = fields.Date.today()
        context['default_customer_id'] = self.second_party.id
        context['default_alarm_line_ids'] = self.alarm_line_ids.ids
        context['default_extinguishing_line_ids'] = self.extinguishing_line_ids.ids
        context['default_is_from_contract'] = True
        return {
            'name': _('Scheduling Visit Wizard'),
            'view_mode': 'form',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'res_model': 'scheduling.visit.wiz',
            'view_id': self.env.ref('visit_management_module.view_scheduling_visit_wizard_form').id,
            'target': 'new',
            'domain': domain,
            'context': context,
        }