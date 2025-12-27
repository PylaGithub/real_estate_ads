from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string="Title", required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancel', 'Cancelled')
    ], default='new', string="Status")

    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    description = fields.Text(string="Description")

    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", default=fields.Date.context_today)
    expected_price = fields.Float(string="Expected Price")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer", store=True)
    selling_price = fields.Float(string="Selling Price")

    bedrooms = fields.Integer(string="Bedrooms")
    garden = fields.Boolean(string="Garden", default=False)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    living_area = fields.Integer(string="Living Area (sqm)")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string="Salesperson")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    phone = fields.Char(string="Phone")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = (rec.living_area or 0) + (rec.garden_area or 0)

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for rec in self:
            rec.best_offer = max(rec.offer_ids.mapped('price') or [0])

    def action_accept(self):
        self.ensure_one()
        if self.state not in ['cancel', 'sold']:
            self.state = 'sold'

    def action_cancel(self):
        self.ensure_one()
        if self.state != 'sold':
            self.state = 'cancel'


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    name = fields.Char(string="Title", required=True)


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'

    name = fields.Char(string="Tag", required=True)
