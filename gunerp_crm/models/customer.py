# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class Customer(models.Model):
  _inherit = "res.partner"

  def _default_country(self):
    return self.env['res.country'].browse(self.env['res.country'].search([('code', '=', 'MN')], limit=1).id)

  state = fields.Selection(
    [('register', 'Бүртгэл баталгаажаагүй'),
      ('register_ok', 'Бүртгэл баталгаажсан'),
      ('register_paid', 'Төлбөр төлөгдсөн')], string='Төлөв', default="register")
  register_type = fields.Selection(
    [('self', 'Биечлэн'),
      ('website', 'Вэб сайтаар'),
      ('facebook', 'Фэйсбүүкээр')], string='Бүртгэлийн суваг')
  customer_main = fields.Boolean(string='Is a Customer Main', default=True)
  last_name = fields.Char()
  first_name = fields.Char()
  gender = fields.Selection(
    [('male', 'Эрэгтэй'),
      ('female', 'Эмэгтэй'),
      ('other', 'Бусад')], string='Хүйс')
  id_card = fields.Char()
  social_facebook = fields.Char()
  id_card_image = fields.Binary("Иргэний үнэмлэхний хуулбар", attachment=True,
        help="This field holds the image used as avatar for this contact, limited to 1024x1024px")
  country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', default=_default_country)
  card_extend_ids = fields.One2many('res.partner.card_extend', 'partner_id', string='Картын төлбөр', copy=True)
  paid_last_date = fields.Date(string='Сүүлд төлбөр төлсөн огноо', compute='_compute_paid_last_date')
  expiry_date = fields.Date(string='Карт дуусах огноо', compute='_compute_expiry_last_date')
  is_expired = fields.Boolean(string='Карт дуусах огноо', compute='_compute_expiry_last_date')

  @api.onchange('last_name','first_name')
  def _onchange_last_first_name(self):
    self.name = '%s %s' % (self.last_name, self.first_name)

  @api.multi
  def action_customer_ok(self):
    self.write({'state': 'register_ok'})

  @api.multi
  def action_customer_paid(self):
    self.write({'state': 'register_paid'})

  def _compute_paid_last_date(self):
    for record in self:
      card_extends = self.env['res.partner.card_extend'].search([('partner_id', '=', record.id)], order='paid_date desc', limit=1)
      record.paid_last_date = card_extends.paid_date

  def _compute_expiry_last_date(self):
    for record in self:
      card_extends = self.env['res.partner.card_extend'].search([('partner_id', '=', record.id)], order='expiry_date desc', limit=1)
      record.expiry_date = card_extends.expiry_date
      # _logger.warning('GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG ---- %s', card_extends.expiry_date)
      # if card_extends.expiry_date:
      #   record.is_expired = datetime.strptime(card_extends.expiry_date, '%Y-%m-%d').date() < datetime.today()

  # @api.onchange('card_extend_ids.paid_date')
  # def _onchange_card_extend_ids(self):
  #   card_extends = self.env['res.partner.card_extend'].search([('partner_id', '=', self._origin.id)], order='paid_date desc', limit=1)
  #   # _logger.warning('GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG ---- %s', card_extends)
  #   # self.paid_last_date = card_extends.paid_date
  #   self.paid_last_date = self.card_extend_ids.paid_date

class CustomerCardExtend(models.Model):
  _name = "res.partner.card_extend"

  partner_id = fields.Many2one('res.partner', string = "Худалдан авагч", required=True)
  paid_date = fields.Date(string="Төлбөр төлсөн огноо", required=True)
  duration_year = fields.Integer(string="Сунгах жил", default=1, required=True)
  expiry_date = fields.Date(string="Дуусах огноо", required=True)

  @api.onchange('paid_date','duration_year')
  def _onchange_paid_date_duration(self):
    if self.paid_date and self.duration_year:
      self.expiry_date = (datetime.strptime(self.paid_date,'%Y-%m-%d') + relativedelta(months=(self.duration_year*12))).strftime('%Y-%m-%d')
      self.partner_id.paid_last_date = self.paid_date
      # self.env['res.partner'].browse(self.partner_id).paid_last_date = self.paid_date
      # self.partner_id.paid_last_date = self.paid_date
      # self.expiry_date.expiry_date = self.expiry_date
