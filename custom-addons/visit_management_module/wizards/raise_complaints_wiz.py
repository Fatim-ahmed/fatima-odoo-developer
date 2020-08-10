# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RaiseComplaintsWiz(models.TransientModel):
    _name = 'raise.complaints.wiz'

    visit_id = fields.Many2one('visit.management')
    maintenance_id = fields.Many2one('maintenance.management')
    customer = fields.Many2one('res.partner', string='Customer')
    num = fields.Char(string='Serial')
    responsible = fields.Many2one('res.users', string='Responsible')
    date = fields.Date('Date')
    complaint = fields.Selection([('no_receives', 'No One Receives The Report'), ('close', 'Place is closed'),
                                  ('other', 'Other')], string='Complaint', default='no_receives')
    other = fields.Char(string='')
    type =  fields.Selection([('visit', 'Visit'), ('maintenance', 'Maintenance')], string='Type')

    def action_create_complaints(self):
        self.env['raise.complaints'].create({'visit_id': self.visit_id.id, 'maintenance_id': self.maintenance_id.id,
                                             'customer': self.customer.id, 'responsible': self.responsible.id,
                                             'date':self.date,'complaint':self.complaint,'other':self.other,
                                             'type':self.type})
