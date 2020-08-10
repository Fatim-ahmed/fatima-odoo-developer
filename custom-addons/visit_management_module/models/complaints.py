# -*- coding: utf-8 -*-

# from datetime import date, datetime, timedelta

from odoo import api, fields, models, _

class RaiseComplaints(models.Model):
    _name = 'raise.complaints'
    _inherit = ['mail.thread']
    _rec_name = 'num'


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


    def fetch_sequence(self, data=None):
        '''generate transaction sequence'''
        return self.env['ir.sequence'].get('raise.complaints')

    @api.model
    def create(self, vals):
        seq = self.fetch_sequence()
        vals['num'] = seq
        return super(RaiseComplaints, self).create(vals)
