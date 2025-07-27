from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MaterialRegistration(models.Model):
    _name = 'material.registration'
    _description = 'Model Material Registration'
    
    material_code = fields.Char(
        string='Material Code',
        required=True,
        index=True,
        help='Unique code for the material'
    )
    
    material_name = fields.Char(
        string='Material Name',
        required=True,
        help='Name of the material'
    )
    
    material_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')
    ], string='Material Type', required=True, help='Type of material')
    
    material_buy_price = fields.Float(
        string='Material Buy Price',
        required=True,
        help='Purchase price of the material'
    )
    
    supplier_id = fields.Many2one(
        'res.partner',
        string='Related Supplier',
        required=True,
        domain=[('is_company', '=', True), ('supplier_rank', '>', 0)],
        help='Supplier of the material'
    )
    
    # Additional fields for better tracking
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    
    _sql_constraints = [
        ('material_code_unique', 'UNIQUE(material_code)', 'Material Code must be unique!'),
    ]
    
    @api.constrains('material_buy_price')
    def _check_material_buy_price(self):
        for record in self:
            if record.material_buy_price < 100:
                raise ValidationError("Material Buy Price must be at least 100!")
    
    @api.constrains('material_code')
    def _check_material_code(self):
        for record in self:
            if not record.material_code or not record.material_code.strip():
                raise ValidationError("Material Code cannot be empty!")
