# -*- coding: utf-8 -*-
"""
    billing.py

    this file contain model for billing

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Bool, And, Or


__all__ = ['Resource', 'Project']
__metaclass__ = PoolMeta


class Resource(ModelSQL, ModelView):
    'Resource'
    __name__ = 'project.resource'
    dummy = fields.Numeric('dummy')

class Project(ModelSQL, ModelView):
    'Project'
    __name__ = 'project.work'
    billable = fields.Selection(
        [
            ('billable', 'Billable'),
            ('non billable', 'Non Billable'),
        ],
        'Billable', select=True, states={
            'invisible': Or(Eval('type') != 'project',Bool(Eval('parent'))),
            'required': Eval('type') == 'project',
    }, depends=['type'])
    currency = fields.Many2One('currency.currency', 'currency', states={
        'invisible': Or(Eval('type') != 'project',Bool(Eval('parent'))),
        'required': Eval('type') == 'project',
    }, depends=['type'])
    hr_rate = fields.Numeric('Hourly Rate', states={
        'invisible': Or(Eval('type') != 'project',Bool(Eval('parent'))),
        'required': Eval('type') == 'project',
    }, depends=['type'])
