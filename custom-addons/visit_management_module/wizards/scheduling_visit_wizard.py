98# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api


class SchedulingVisit(models.TransientModel):
    _name = 'scheduling.visit.wiz'

    contract_id = fields.Many2one('contract.maintenance', stirng='Contract')
    first_visit_date = fields.Date('Date Of First Visit')
    visit_num = fields.Integer(related='contract_id.visit_numb', string='Visit Number')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    customer_id = fields.Many2one('res.partner', string='Customer')
    extinguishing_line_ids = fields.Many2many('extinguishing.system.line', string='Extinguishing System')
    alarm_line_ids = fields.Many2many('alarm.system.line', string='Alarm System')
    is_from_contract = fields.Boolean("From Contract", defualt=False)

    def action_create_visit(self):
        ids=[]
        for i in range(self.visit_num):
            y = 30
            y = y * i
            second_visit = fields.Date.to_string(fields.Date.from_string(str(self.first_visit_date)) + timedelta(days=y))
            visit = self.env['visit.management'].create({'state': 'draft', 'date': second_visit,
                                                         'customer': self.customer_id.id,
                                                         'responsible': self.responsible_id.id,
                                                         'contract_id': self.contract_id.id})
            alarm_line_ids = [(0, 0, {'name': line.name.id, 'count': 0, 'contract_id':False,'visit_id': visit.id}) for line in self.alarm_line_ids]
            extinguishing_line_ids = [(0, 0, {'name': line.name.id, 'count': 0, 'contract_id':False,'visit_id': visit.id}) for line in self.extinguishing_line_ids]
            visit.write({'extinguishing_line_ids':extinguishing_line_ids, 'alarm_line_ids':alarm_line_ids})
            ids.append(visit.id)
        action = self.env.ref('visit_management_module.visit_action').read()[0]
        action['domain'] = [
            ('id', 'in', ids),
        ]
        return action

    @api.onchange('contract_id')
    def set_line_ids(self):
        self.extinguishing_line_ids = self.contract_id.extinguishing_line_ids.ids
        self.alarm_line_ids = self.contract_id.alarm_line_ids.ids