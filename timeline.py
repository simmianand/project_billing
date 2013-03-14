# -*- coding: utf-8 -*-
"""
    Timeline

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval, Not


__all__ = ['Timeline']
__metaclass__ = PoolMeta


class Timeline:
    __name__ = 'timesheet.line'
    billing_type = fields.Selection([
        ('billable', 'Billable'),
        ('non billable', 'Non Billable'),
    ], 'Billing Type', required=True, select=True,
    states={'readonly': Not(Eval('billing_type') == 'billable')
    })

    @staticmethod
    def default_billing_type():
            return Transaction().context.get('billable')

