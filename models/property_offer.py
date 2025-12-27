from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status")

    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity (Days)", default=7)
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline', store=True)
    creation_date = fields.Date(string="Creation Date", default=fields.Date.context_today)

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = 0

    @api.constrains('deadline')
    def _check_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date and rec.deadline <= rec.creation_date:
                raise ValidationError(_("Deadline must be after the creation date."))

    def action_accept(self):
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.selling_price = rec.price
            rec.property_id.buyer_id = rec.partner_id
            rec.property_id.state = 'accepted'

    def action_refuse(self):
        for rec in self:
            rec.status = 'refused'
