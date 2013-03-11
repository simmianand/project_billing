# -*- coding: utf-8 -*-
"""
    billing.py

    this file contain model for billing

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta


__all__ = ['Resource', 'TopProject']
__metaclass__ = PoolMeta


class Resource(ModelSQL, ModelView):
    __name__ = 'project.resource'
    dummy = fields.Numeric('dummy')

class TopProject(ModelSQL, ModelView):
    __name__ = 'project.topproject'
    dummy = fields.Numeric('dummy')
