# -*- coding: utf-8 -*-

# from datetime import date, datetime, timedelta

from odoo import api, fields, models, _


# from odoo.exceptions import UserError


class CommonContract(models.Model):
    """ Model for case stages. This models the main stages of a Maintenance Request management flow. """

    _name = 'common.contract'
    _description = 'common filed between contract type'

    name = fields.Char('Name', required=True, translate=True)
    num = fields.Char('Sequence')
    date = fields.Date('Date', default=fields.Date.today)
    first_party = fields.Many2one('res.partner', string='First party')
    first_party_phone = fields.Char(related='first_party.phone', string='Phone')
    first_party_com_register = fields.Char(related='first_party.commercial_register', string='Commercial Register')
    first_party_executive_manager = fields.Char(related='first_party.executive_manager')
    first_party_exec_mag_id = fields.Char(related='first_party.exec_mag_id')
    second_party = fields.Many2one('res.partner', string='Second Party')
    second_party_phone = fields.Char(related='second_party.phone', string='Phone')
    second_party_com_register = fields.Char(related='second_party.commercial_register', string='Commercial Register')
    second_party_executive_manager = fields.Char(related='second_party.executive_manager')
    second_party_exec_mag_id = fields.Char(related='second_party.exec_mag_id')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State', default='draft')
    contract_amount = fields.Float(string='Amount')

    def get_arabic_name_day(self, day):
        day_name = ''
        if day == 'Wednesday':
            day_name = 'يَوم الأربعاء'
        if day == 'Thursday':
            day_name = 'يَوم الخميس'
        if day == 'Sunday':
            day_name = 'يَوم الأحَد'
        if day == 'Monday':
            day_name = 'يَوم الإثنين'
        if day == 'Tuesday':
            day_name = 'يَوم الثلاثاء'
        if day == 'Friday':
            day_name = 'يَوم الجمعة'
        if day == 'Saturday':
            day_name = 'يَوم السبت'
        return day_name


class ContractAgreement(models.Model):
    _name = 'contract.agreement'
    _inherit = ['common.contract','mail.thread']
    _description = 'Agreement contract'

    order_id = fields.Many2one('sale.order', string='Sale Order')
    amount_untaxed = fields.Monetary(related='order_id.amount_untaxed')
    amount_tax = fields.Monetary(related='order_id.amount_tax')
    amount_total = fields.Monetary(related='order_id.amount_total')
    currency_id = fields.Many2one('res.currency', related='order_id.currency_id')
    note = fields.Html(string='Other Condition')
    line_ids = fields.Many2many('sale.order.line', string='Order Lines', compute='get_lines_ids', store=True)
    duration = fields.Html("Duration")
    installment_ids = fields.One2many('contract.installment', 'contract_id', string='Installments')

    def create_maintenance_contract(self):
        self.env['contract.maintenance'].create({'name': self.name, 'contract_amount': self.amount_total, 'first_party': self.first_party.id,
                                                 'second_party': self.second_party.id})

    def fetch_sequence(self, data=None):
        '''generate transaction sequence'''
        return self.env['ir.sequence'].get('agreement.contract')

    @api.depends('order_id')
    def get_lines_ids(self):
        for rec in self:
            if rec.order_id:
                list_ids = self.env['sale.order.line'].sudo().search([('order_id', '=', rec.order_id.id)]).ids
                rec.line_ids = [(6, 0, list_ids)]

    @api.model
    def create(self, vals):
        seq = self.fetch_sequence()
        vals['num'] = seq
        return super(ContractAgreement, self).create(vals)


class ContractMaintenance(models.Model):
    _name = 'contract.maintenance'
    _inherit = ['common.contract','mail.thread']
    _description = 'maintenance contract'

    note = fields.Html(string='Other Condition')
    duration = fields.Html("Duration")
    alarm_line_ids = fields.One2many('alarm.system.line', 'contract_id', string='Alarm System')
    extinguishing_line_ids = fields.One2many('extinguishing.system.line', 'contract_id', string='Extinguishing System')
    pumps = fields.Boolean('Pumps', default=True)
    fire_boxes = fields.Boolean('Fire boxes', default=True)
    fixed_automatic_systems = fields.Boolean('Fixed automatic systems', default=True)
    fire_extinguishers = fields.Boolean('Fire extinguishers', default=True)
    internal_external_fire_socket_systems = fields.Boolean('Internal and external fire socket systems', default=True)
    eq_co_con_fire_protect_sys = fields.Boolean('Equipment, cocks, and connections for fire protection systems', default=True)
    fire_pump_board = fields.Boolean('Fire pump board', default=True)
    main_alarm_panel = fields.Boolean('Main alarm panel', default=True)
    sign_board = fields.Boolean('Sign board', default=True)
    panel_help_signals = fields.Boolean('Panel help signals', default=True)
    fire_detectors = fields.Boolean('Fire detectors', default=True)
    signal_lamps_help = fields.Boolean('Signal lamps help', default=True)
    call_points_hand = fields.Boolean('Call points Hand', default=True)
    audio_visual_alarms = fields.Boolean('Audio and visual alarms', default=True)
    generator = fields.Boolean('Backup electrical source (generator)', default=True)
    fire_chokes = fields.Boolean('Fire Chokes', default=True)
    emergency_lighting = fields.Boolean('Emergency lighting', default=True)
    air_fans_push_emergency_ladder = fields.Boolean('Air fans push emergency ladders', default=True)
    basement_suction_fans = fields.Boolean('Basement and suction fans', default=True)
    electrical_wiring_network = fields.Boolean('Electrical wiring network', default=True)
    end_date = fields.Date('End Date')
    visit_numb = fields.Integer('Number Of Visit')

    def fetch_sequence(self, data=None):
        '''generate transaction sequence'''
        return self.env['ir.sequence'].get('maintenance.contract')

    @api.model
    def create(self, vals):
        seq = self.fetch_sequence()
        vals['num'] = seq
        return super(ContractMaintenance, self).create(vals)

    def get_alarm_text(self):
        final_text = ''
        if self.pumps:
            final_text += 'المضخات' + '-'
        if self.fire_boxes:
            final_text += ' صناديق الحريق' + '-'
        if self.fixed_automatic_systems:
            final_text += ' الانظمة التلقائية الثابتة'+'-'
        if self.fire_extinguishers:
            final_text += 'طفايات الحريق' + '-'
        if self.internal_external_fire_socket_systems:
            final_text += 'أنظمة مأخذ الحريق الداخلية والخارجية' + '-'
        if self.eq_co_con_fire_protect_sys:
            final_text += ' المعدات والمحابس والتوصيلات الخاصة بنظم الحماية من الحريق'+'-'
        if self.fire_pump_board:
            final_text += 'اللوحة الخاصة بمضخة الحريق'
        return final_text

    def get_extinguishing_text(self):
        final_text = ''
        if self.main_alarm_panel:
            final_text += 'لوحة الانذار الرئيسية' + '-'
        if self.sign_board:
            final_text += ' لوحة الاشارات' + '-'
        if self.panel_help_signals:
            final_text += ' لوحة الاشارات المساعدة'+'-'
        if self.fire_detectors:
            final_text += ' كاشفات الحريق' + '-'
        if self.signal_lamps_help:
            final_text += ' مصابيح الاشارة المساعدة' + '-'
        if self.call_points_hand:
            final_text += ' نقاط النداء اليدوية'+'-'
        if self.audio_visual_alarms:
            final_text += ' اجهزة التنبيه السمعية والمرئية'+'-'
        if self.generator:
            final_text += 'المصدر الكهربائي الاحتياطي(المولد)'+'-'
        if self.fire_chokes:
            final_text += '  خوانق الحريق'+'-'
        if self.emergency_lighting:
            final_text += ' انارة الطوارئ'+'-'
        if self.air_fans_push_emergency_ladder:
            final_text += ' مراوح دفع الهواء بسلالم الطوارئ'+'-'
        if self.basement_suction_fans:
            final_text += ' مراوح شفط ودفع الهواء بالبدروم'+'-'
        if self.electrical_wiring_network:
            final_text += ' شبكة التمديدات الكهربائية'
        return final_text


class ContractInstallment(models.Model):
    _name = 'contract.installment'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    amount = fields.Float(string='Amount')
    contract_id = fields.Many2one(string='Contract')


class AlarmSystemLine(models.Model):
    _name = 'alarm.system.line'

    name = fields.Many2one('system.type.value', string='Name')
    is_available = fields.Boolean(string='Is Available ?')
    not_available = fields.Boolean(string='Is Not Available ?')
    count = fields.Float(string='Count')
    note = fields.Text(string='Note')
    contract_id = fields.Many2one('contract.maintenance')


class ExtinguishingSystemLine(models.Model):
    _name = 'extinguishing.system.line'

    name = fields.Many2one('system.type.value', string='Name')
    is_available = fields.Boolean(string='Is Available ?')
    not_available = fields.Boolean(string='Is Not Available ?')
    count = fields.Float(string='Count')
    note = fields.Text(string='Note')
    contract_id = fields.Many2one('contract.maintenance')


class SystemTypeValue(models.Model):
    _name = 'system.type.value'

    name = fields.Char(string="Name")
    is_extinguishing = fields.Boolean('Is Extinguishing ?')
