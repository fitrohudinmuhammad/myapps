from unittest.mock import patch

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestMaterialRegistration(TransactionCase):    
    def setUp(self):
        super(TestMaterialRegistration, self).setUp()
        
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'is_company': True,
            'supplier_rank': 1,
        })
        
        self.test_material_data = {
            'material_code': 'MAT001',
            'material_name': 'Test Fabric',
            'material_type': 'fabric',
            'material_buy_price': 150.0,
            'supplier_id': self.supplier.id,
        }
    
    def test_create_material_success(self):
        material = self.env['material.registration'].create(self.test_material_data)
        
        self.assertEqual(material.material_code, 'MAT001')
        self.assertEqual(material.material_name, 'Test Fabric')
        self.assertEqual(material.material_type, 'fabric')
        self.assertEqual(material.material_buy_price, 150.0)
        self.assertEqual(material.supplier_id, self.supplier)
    
    def test_material_buy_price_constraint(self):
        with self.assertRaises(ValidationError):
            self.test_material_data['material_buy_price'] = 50.0
            self.env['material.registration'].create(self.test_material_data)
    
    def test_material_code_unique_constraint(self):
        self.env['material.registration'].create(self.test_material_data)
        
        with self.assertRaises(Exception):
            self.env['material.registration'].create(self.test_material_data)
    
    def test_required_fields(self):
        required_fields = ['material_code', 'material_name', 'material_type', 'material_buy_price', 'supplier_id']
        
        for field in required_fields:
            test_data = self.test_material_data.copy()
            del test_data[field]
            
            with self.assertRaises(Exception):
                self.env['material.registration'].create(test_data)
    
    def test_material_type_selection(self):
        valid_types = ['fabric', 'jeans', 'cotton']
        
        for material_type in valid_types:
            test_data = self.test_material_data.copy()
            test_data['material_type'] = material_type
            test_data['material_code'] = f'MAT_{material_type.upper()}'
            
            material = self.env['material.registration'].create(test_data)
            self.assertEqual(material.material_type, material_type)
    
    def test_update_material(self):
        material = self.env['material.registration'].create(self.test_material_data)
        
        material.write({
            'material_name': 'Updated Fabric',
            'material_buy_price': 200.0,
        })
        
        self.assertEqual(material.material_name, 'Updated Fabric')
        self.assertEqual(material.material_buy_price, 200.0)
    
    def test_delete_material(self):
        material = self.env['material.registration'].create(self.test_material_data)
        material_id = material.id
        
        material.unlink()
        
        deleted_material = self.env['material.registration'].browse(material_id)
        self.assertFalse(deleted_material.exists())

    def test_search_by_material_type(self):
        fabric_data = self.test_material_data.copy()
        fabric_data['material_code'] = 'FAB001'
        
        jeans_data = self.test_material_data.copy()
        jeans_data['material_code'] = 'JEA001'
        jeans_data['material_type'] = 'jeans'
        
        cotton_data = self.test_material_data.copy()
        cotton_data['material_code'] = 'COT001'
        cotton_data['material_type'] = 'cotton'
        
        fabric_material = self.env['material.registration'].create(fabric_data)
        jeans_material = self.env['material.registration'].create(jeans_data)
        cotton_material = self.env['material.registration'].create(cotton_data)
        
        fabric_materials = self.env['material.registration'].search([('material_type', '=', 'fabric')])
        jeans_materials = self.env['material.registration'].search([('material_type', '=', 'jeans')])
        cotton_materials = self.env['material.registration'].search([('material_type', '=', 'cotton')])
        
        self.assertIn(fabric_material, fabric_materials)
        self.assertIn(jeans_material, jeans_materials)
        self.assertIn(cotton_material, cotton_materials)
    
    def test_supplier_domain(self):
        material = self.env['material.registration'].create(self.test_material_data)
        self.assertTrue(material.supplier_id.is_company)
        self.assertTrue(material.supplier_id.supplier_rank > 0)

