# -*- coding: utf-8 -*-
"""
    

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta


__all__ = ['Timeline']
__metaclass__ = PoolMeta


class Timeline(ModelSQL, ModelView):
    __name__ = 'project.timeline'
    dummy = fields.Numeric('dummy')
