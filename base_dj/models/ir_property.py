# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class Property(models.Model):

    _inherit = 'ir.property'

    @api.multi
    def _update_values(self, values):
        if self.env.context.get('xmlid_value_reference', False):
            record = self.env.ref(values.get('value_reference'))
            value = u'%s,%i' % (record._name, record.id)
            values['value_reference'] = value
        return super(Property, self)._update_values(values)

    @api.multi
    def _export_rows(self, fields):
        res = super(Property, self)._export_rows(fields)
        position = fields.index([u'value_reference'])
        for row in res:
            reference = row[position]
            if reference:
                ref_list = reference.split(',')
                model_data = self.env['ir.model.data'].search(
                    [('model', '=', ref_list[0]),
                     ('res_id', '=', ref_list[1])], limit=1)
                xmlid = u'%s.%s' % (model_data.module, model_data.name)
                row[position] = xmlid
        return res
