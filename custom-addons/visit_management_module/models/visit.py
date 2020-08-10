# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# from odoo.exceptions import UserError


class CommonVisitMaintenance(models.Model):
    """ Model for case stages. This models the main stages of a Maintenance Request management flow. """

    _name = 'common.visit.maintenance'
    _description = 'common filed between visit and maintenance request'

    num = fields.Char(string='Serial')
    note = fields.Html(string='Note')
    date = fields.Date('Date')
    customer = fields.Many2one('res.partner', string='Customer')
    responsible = fields.Many2one('res.users', string='Responsible')
    receiver_person = fields.Char(string='Receiver')
    signature = fields.Binary(string='Signature')
    contract_id = fields.Many2one('contract.maintenance', string='Contract')
    state = fields.Selection([('draft', 'Draft'), ('progress', 'In Progress'), ('delay', 'Delay'), ('done', 'Done')],
                             string='State', default='draft',track_visibility='onchange')
    is_additional = fields.Boolean('Additional', defualt=False)

    def action_progress(self):
        self.state='progress'

    def action_done(self):
        self.state='done'

    def set_to_draft(self):
        self.state = 'draft'

class VisitManagement(models.Model):
    _name = 'visit.management'
    _inherit = ['common.visit.maintenance', 'mail.thread']
    _description = 'visit management'
    _rec_name = 'num'

    status = fields.Selection([('work', 'Work'), ('not', 'Not Work')], string='', default='work')
    alarm_line_ids = fields.One2many('alarm.system.line', 'visit_id', string='Alarm System')
    actual_date = fields.Date('Actual Date')
    extinguishing_line_ids = fields.One2many('extinguishing.system.line', 'visit_id', string='Extinguishing System')

    def action_progress(self):
        res = super(VisitManagement, self).action_progress()
        records = self.env['visit.management'].search([('id', '!=', self.id), ('contract_id', '=', self.contract_id.id),
                                                       ('customer', '=', self.customer.id),
                                                       ('is_additional', '=', False),
                                                       ('date', '<', self.date),('state','!=','done')])
        if records:
            raise ValidationError(_('You cannot change the current visit to progress unless the previous visit done'))
        else:
            self.actual_date = fields.Date.today()
            return res

    def action_delay_visit(self):
        records = self.env['visit.management'].search([('state','=','draft'),('is_additional','=',False)])
        for rec in records:
            to_day = fields.Date.today()
            if rec.date < to_day:
                rec.state='delay'

    @api.constrains('contract_id','customer','responsible','date')
    def check_state(self):
        for rec in self:
            records =  self.env['visit.management'].search([('id','!=',rec.id),('contract_id','=',rec.contract_id.id),
                                                           ('customer','=', rec.customer.id),('is_additional','=',False),
                                                           ('date','<=',rec.date)])
            if records:
                for visit in records:
                    record_date_month = datetime.strptime(str(visit.date), "%Y-%m-%d").month
                    rec_date_month = datetime.strptime(str(rec.date), "%Y-%m-%d").month
                    if record_date_month == rec_date_month:
                        raise ValidationError(_('You cant not create 2 Visit for same contract and customer in the same months'))

    def action_raise_complaints(self):
        domain = []
        context = {}
        context = dict(self.env.context or {})
        context['default_visit_id'] = self.id
        context['default_date'] = fields.Date.today()
        context['default_customer'] = self.customer.id
        context['default_responsible'] = self.responsible.id
        context['default_type'] = 'visit'
        return {
            'name': _('Raise Complaints'),
            'view_mode': 'form',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'res_model': 'raise.complaints.wiz',
            'view_id': self.env.ref('visit_management_module.view_raise_complaints_wizard_form').id,
            'target': 'new',
            'domain': domain,
            'context': context,
        }

    def create_maintenance_request(self):
        maintenance = self.env['maintenance.management'].create({'contract_id': self.contract_id.id, 'responsible': self.responsible.id,
                                                   'customer': self.customer.id})
        alarm_line_ids = [(0, 0, {'name': line.name.id, 'count': 0, 'contract_id':False,'visit_id': False,'maintenance_id':maintenance.id}) for line in self.alarm_line_ids]
        extinguishing_line_ids = [(0, 0, {'name': line.name.id, 'count': 0, 'contract_id':False,'visit_id': False,'maintenance_id':maintenance.id}) for line in self.extinguishing_line_ids]
        maintenance.write({'extinguishing_line_ids':extinguishing_line_ids, 'alarm_line_ids':alarm_line_ids})
        action = self.env.ref('visit_management_module.maintenance_action').read()[0]
        action['domain'] = [('id', '=', maintenance.id),]
        return action

    def fetch_sequence(self, data=None):
        '''generate transaction sequence'''
        return self.env['ir.sequence'].get('visit.management')

    @api.model
    def create(self, vals):
        seq = self.fetch_sequence()
        contract_id = vals.get('contract_id')
        final_seq = seq
        if contract_id:
            final_seq = ''
            contract_seq = self.env['contract.maintenance'].sudo().browse(contract_id).read(['num'])
            contract_seq = contract_seq[0]['num']
            final_seq = contract_seq+'/'+seq
        vals['num'] = final_seq
        return super(VisitManagement, self).create(vals)


class MaintenanceManagement(models.Model):
    _name = 'maintenance.management'
    _inherit = ['common.visit.maintenance', 'mail.thread']
    _description = 'Maintenance Management'
    _rec_name = 'num'

    alarm_line_ids = fields.One2many('alarm.system.line', 'maintenance_id', string='Alarm System')
    visit_id = fields.Many2one('visit.management', string="Visit")
    extinguishing_line_ids = fields.One2many('extinguishing.system.line', 'maintenance_id', string='Extinguishing System')

    def create_sale_order(self):
        order = self.env['sale.order'].create({'partner_id': self.customer.id})
        action = self.env.ref('sale.action_orders').read()[0]
        action['domain'] = [('id', '=', order.id)]
        return action

    def action_raise_complaints(self):
        domain = []
        context = {}
        context = dict(self.env.context or {})
        context['default_maintenance_id'] = self.id
        context['default_date'] = fields.Date.today()
        context['default_customer'] = self.customer.id
        context['default_responsible'] = self.responsible.id
        context['default_type'] = 'maintenance'
        return {
            'name': _('Raise Complaints'),
            'view_mode': 'form',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'res_model': 'raise.complaints.wiz',
            'view_id': self.env.ref('visit_management_module.view_raise_complaints_wizard_form').id,
            'target': 'new',
            'domain': domain,
            'context': context,
        }

    def fetch_sequence(self, data=None):
        '''generate transaction sequence'''
        return self.env['ir.sequence'].get('maintenance.management')

    @api.model
    def create(self, vals):
        seq = self.fetch_sequence()
        vals['num'] = seq
        return super(MaintenanceManagement, self).create(vals)


class AlarmSystemLine(models.Model):
    _inherit = 'alarm.system.line'

    visit_id = fields.Many2one('visit.management')
    maintenance_id = fields.Many2one('maintenance.management')


class ExtinguishingSystemLine(models.Model):
    _inherit = 'extinguishing.system.line'

    visit_id = fields.Many2one('visit.management')
    maintenance_id = fields.Many2one('maintenance.management')
