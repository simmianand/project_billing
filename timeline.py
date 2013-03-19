# -*- coding: utf-8 -*-
"""
    Timeline

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import fields, ModelView, ModelSQL
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval, Not, Bool, And


__all__ = ['Timeline', 'Timesheet']
__metaclass__ = PoolMeta


class Timeline(ModelSQL, ModelView):
    '''Extending Timesheet_lines
    '''
    __name__ = 'timesheet.line'
    billing_type = fields.Selection([
        ('billable', 'Billable'),
        ('non billable', 'Non Billable'),
    ], 'Billing Type', select=True, required=True, states={
        'readonly': And(Not(Eval('billing_type') == 'billable'),
        Bool(Eval('billing_type'))),
    })

    @staticmethod
    def default_billing_type():
        '''Takes default selected value in timesheet
        '''
        return Transaction().context.get('billable')


class Timesheet(ModelSQL, ModelView):
    __name__ = 'project.work'
    timesheet_lines = fields.One2Many(
        'timesheet.line', 'work', 'Timesheet Lines',
        depends=['timesheet_available', 'active', 'billable'],
        states={
            'invisible': Not(Bool(Eval('timesheet_available'))),
            'readonly': Not(Bool(Eval('active'))),
        }, context={'billable': Eval('billable')},
    )
    children = fields.One2Many(
        'project.work', 'parent', 'Children',
        context={'billable': Eval('billable')}, depends=['billable'],
    )

    @staticmethod
    def default_billable():
        '''Takes default selected value in task's timesheet
        '''
        if Transaction().context.get('billable'):
            return Transaction().context.get('billable')
