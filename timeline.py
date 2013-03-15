# -*- coding: utf-8 -*-
"""
    Timeline

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval, Not, Bool, And


__all__ = ['Timeline']
__metaclass__ = PoolMeta


class Timeline:
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
