# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)

class User(models.Model):
  _inherit = "res.users"

  @api.model
  def create(self, vals):
    user = super(User, self).create(vals)
    user.partner_id.customer = self.env.context.get('is_customer', False)
    return user
