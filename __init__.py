# -*- coding: utf-8 -*-
"""
    __init__

    Initilize project_billing

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool

from .billing import Resource, Project
from .timeline import Timeline


def register():
    """This function will register trytond module project_billing
    """
    Pool.register(
        Resource,
        Project,
        Timeline,
        module='projectbilling', type_='model',
    )
