# -*- coding: utf-8 -*-
"""
    

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Timeline']
__metaclass__ = PoolMeta


class Timeline:
    __name__ = 'timesheet.line'

    billing_type = fields.Selection([
        ('billable', 'Billable'),
        ('non billable', 'Non Billable'),
    ], 'Billing Type', required=True, select=True)
