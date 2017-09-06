# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, api
from ..utils import create_zipfile, make_title


class Collection(models.Model):
    """A collection of compilations."""

    _name = 'dj.collection'
    _inherit = 'dj.download.mixin'
    _dj_download_path = '/dj/download/collection/'

    name = fields.Char()
    album_ids = fields.One2many(
        string='Albums',
        comodel_name='dj.collection.album',
        inverse_name='collection_id',
    )

    @api.multi
    def burn(self):
        """Burn collection box into a zip file."""
        self.ensure_one()
        files = self.get_all_discs()
        zf = create_zipfile(files)
        filename = self.make_box_title()
        return filename, zf.read()

    def make_box_title(self):
        return make_title(self.name, 'box')

    def get_all_discs(self):
        files = []
        for comp in self.album_ids.mapped('compilation_id'):
            files.extend(comp.get_all_tracks())
        return files


class CollectionAlbum(models.Model):
    _name = 'dj.collection.album'
    _rec_name = 'compilation_id'
    _order = 'sequence asc'

    collection_id = fields.Many2one(
        comodel_name='dj.collection',
        string='Collection',
    )
    compilation_id = fields.Many2one(
        comodel_name='dj.compilation',
        string='Compilation',
        required=True,
    )
    sequence = fields.Integer(
        'Sequence',
        help="Sequence for the handle.",
        default=10
    )
