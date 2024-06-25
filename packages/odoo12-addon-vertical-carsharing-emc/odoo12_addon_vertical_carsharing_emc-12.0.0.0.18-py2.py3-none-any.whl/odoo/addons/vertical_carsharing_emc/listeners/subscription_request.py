from odoo.addons.component.core import Component


class SubscriptionRequest(Component):
    _name = 'subscription.request.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['subscription.request']
