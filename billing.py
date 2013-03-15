# -*- coding: utf-8 -*-
"""
    billing.py

    this file contain model for billing

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, Bool, And, Or, Not
from trytond.transaction import Transaction

__all__ = ['Resource', 'Project', 'Party']
__metaclass__ = PoolMeta


class Resource(ModelSQL, ModelView):
    'Resource'
    __name__ = 'project.resource'
    project = fields.Many2One('project.work', 'Project')
    employee = fields.Many2One('company.employee', 'Employee', required=True)
    product = fields.Many2One(
        'product.product', 'Product',
        domain=[('type', '=', 'service')],
    )

    @classmethod
    def __setup__(cls):
        super(Resource, cls).__setup__()
        cls._sql_constraints += [
            ('Unique_Resource', 'UNIQUE(employee)',
                'Some employees are remarked as resource for this project'),
        ]


class Party(ModelSQL, ModelView):
    'Party'
    __name__ = 'party.party'

    @classmethod
    def __setup__(cls):
        super(Party, cls).__setup__()
        cls.customer_payment_term.required = True


class Project(ModelSQL, ModelView):
    'Project'
    __name__ = 'project.work'
    billable = fields.Selection(
        [
            ('billable', 'Billable'),
            ('non billable', 'Non Billable'),
        ],
        'Billable', select=True, states={
            'invisible': Or(Eval('type') != 'project', Bool(Eval('parent'))),
            'required': And(Eval('type') == 'project', ~Bool(Eval('parent'))),
        },
        depends=['type', 'parent']
    )
    currency = fields.Many2One('currency.currency', 'Currency', states={
        'invisible': Or(Eval('type') != 'project', Bool(Eval('parent'))),
        'required': And(Eval('type') == 'project', ~Bool(Eval('parent'))),
    }, depends=['type', 'parent'])
    hr_rate = fields.Numeric('Hourly Rate', states={
        'invisible': Or(Eval('type') != 'project', Bool(Eval('parent'))),
        'required': And(Eval('type') == 'project', ~Bool(Eval('parent'))),
    }, depends=['type', 'parent'])
    resources = fields.One2Many('project.resource', 'project', 'Resources')
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

    @classmethod
    def __setup__(cls):
        super(Project, cls).__setup__()
        cls.party.states={
        'required': And(Eval('type') == 'project', ~Bool(Eval('parent'))),
        }
        #cls.party.depends=['type', 'parent']
        #cls.invoice_address.states={
        #'required': And(Eval('type') == 'project', ~Bool(Eval('parent'))),
        #}
        #cls.invoice_address.depends=['type', 'parent']
        cls._buttons.update({
            'createinvoice': {
                'invisible': Eval(1),
            }
        })

    @classmethod
    @ModelView.button
    def createinvoice(cls, projects):
        invoice = Pool().get('account.invoice')
        products = Pool().get('product.product')
        #print products.search_rec_name(name='Openlabs').name
        for project in projects:
            details = {
                'payment_term': project.party.customer_payment_term.id,
                'party': project.party.id,
                'account': project.company.account_receivable.id,
                'invoice_address': cls._get_invoice_address(project.party),
            }
            details['description'] = project.name
            lines = [
                        ('create', {
                                'line': 'line',
                                'quantity': 3,
                                'unit': 30,
                                'divisor': 4,
                                'percentage': 25,
                                'days': 30,
                                })
                    ]
            details['lines'] = lines
            invoice.create(details)
        return True

    @classmethod
    def _get_invoice_address(self, party):
        if party:
            return party.address_get(type='invoice').id
