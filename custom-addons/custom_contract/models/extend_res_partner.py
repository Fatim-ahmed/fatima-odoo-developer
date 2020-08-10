# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    commercial_register = fields.Char('Commercial Register')
    executive_manager = fields.Char('Executive Manager')
    exec_mag_id = fields.Char('Identifier')
    total_agreement = fields.Integer(compute='total_agreement_contract', string="Total Agreement Contract")
    total_main = fields.Integer(compute='total_maint_contract', string="Total Maintenance Contract")

    def action_view_agreement_contract(self):
        self.ensure_one()
        action = self.env.ref('custom_contract.agreement_contract_action').read()[0]
        action['domain'] = [
            ('second_party', 'child_of', self.id),
        ]
        return action

    def action_view_maintenance_contract(self):
        self.ensure_one()
        action = self.env.ref('custom_contract.maintenance_contract_action').read()[0]
        action['domain'] = [
            ('second_party', 'child_of', self.id),
        ]
        return action

    def total_agreement_contract(self):
        contract_ids = self.env['contract.agreement'].search([('second_party', '=', self.id)])
        if contract_ids:
            self.total_agreement = len(contract_ids)
        else:
            self.total_agreement = 0

    def total_maint_contract(self):
        contract_ids = self.env['contract.maintenance'].search([('second_party', '=', self.id)])
        if contract_ids:
            self.self.total_main = len(contract_ids)
        else:
            self.self.total_main = 0

