import json

from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

from werkzeug.wrappers import Response as WerkzeugResponse


class MaterialRegistrationAPI(http.Controller):
    @http.route('/api/materials', type='http', auth='public', methods=['GET'], csrf=False)
    def get_materials(self):
        try:
            materials = request.env['material.registration'].sudo().search([])
            
            result = []
            for material in materials:
                result.append({
                    'id': material.id,
                    'material_code': material.material_code,
                    'material_name': material.material_name,
                    'material_type': material.material_type,
                    'material_buy_price': material.material_buy_price,
                    'supplier_id': material.supplier_id.id,
                    'supplier_name': material.supplier_id.name,
                    'create_date': material.create_date.isoformat() if material.create_date else None,
                    'write_date': material.write_date.isoformat() if material.write_date else None,
                })
            
            return request.make_response(
                json.dumps({'success': True, 'data': result, 'count': len(result)}),
                headers={'Content-Type': 'application/json'}
            )
            
        except Exception as e:
            return request.make_response(
                json.dumps({'error': 'Internal server error'}),
                headers={'Content-Type': 'application/json'},
                status=500
            )
    
    @http.route('/api/materials', type='json', auth='public', methods=['POST'], csrf=False)
    def create_material(self, **kw):
        try:
            data = request.jsonrequest
            
            required_fields = ['material_code', 'material_name', 'material_type', 'material_buy_price', 'supplier_id']
            for field in required_fields:
                if field not in data or data[field] is None or data[field] == '':
                    return {'error': f'Field {field} is required'}
            
            if data['material_type'] not in ['fabric', 'jeans', 'cotton']:
                return {'error': 'Invalid material_type. Must be: fabric, jeans, or cotton'}
            
            try:
                price = float(data['material_buy_price'])
                if price < 100:
                    return {'error': 'Material Buy Price must be at least 100'}
            except (ValueError, TypeError):
                return {'error': 'Material Buy Price must be a valid number'}
            
            try:
                supplier_id = int(data['supplier_id'])
                supplier = request.env['res.partner'].browse(supplier_id)
                if not supplier.exists():
                    return {'error': 'Supplier not found'}
            except (ValueError, TypeError):
                return {'error': 'Supplier ID must be a valid number'}
            
            material = request.env['material.registration'].sudo().create(data)
            
            return {
                'success': True, 
                'message': 'Material created successfully',
                'id': material.id
            }
            
        except ValidationError as e:
            return {'error': str(e)}
        except Exception as e:
            return {'error': 'Internal server error'}
    
    @http.route('/api/materials/<int:material_id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **kw):
        try:
            material = request.env['material.registration'].sudo().browse(material_id)
            if not material.exists():
                return {'error': 'Material not found'}
            
            data = request.jsonrequest
            
            if 'material_type' in data and data['material_type'] not in ['fabric', 'jeans', 'cotton']:
                return {'error': 'Invalid material_type. Must be: fabric, jeans, or cotton'}
            
            if 'material_buy_price' in data:
                try:
                    price = float(data['material_buy_price'])
                    if price < 100:
                        return {'error': 'Material Buy Price must be at least 100'}
                except (ValueError, TypeError):
                    return {'error': 'Material Buy Price must be a valid number'}
            
            if 'supplier_id' in data:
                try:
                    supplier_id = int(data['supplier_id'])
                    supplier = request.env['res.partner'].browse(supplier_id)
                    if not supplier.exists():
                        return {'error': 'Supplier not found'}
                except (ValueError, TypeError):
                    return {'error': 'Supplier ID must be a valid number'}
            
            material.write(data)
            
            return {
                'success': True, 
                'message': 'Material updated successfully'
            }
            
        except ValidationError as e:
            return {'error': str(e)}
        except Exception as e:
            return {'error': 'Internal server error'}
    
    @http.route('/api/materials/<int:material_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id):
        try:
            material = request.env['material.registration'].sudo().browse(material_id)
            if not material.exists():
                return request.make_response(
                    json.dumps({'error': 'Material not found'}),
                    headers={'Content-Type': 'application/json'},
                    status=404
                )
            
            material.unlink()
            
            return request.make_response(
                json.dumps({
                    'success': True, 
                    'message': 'Material deleted successfully'
                }),
                headers={'Content-Type': 'application/json'}
            )
            
        except Exception as e:
            return request.make_response(
                json.dumps({'error': 'Internal server error'}),
                headers={'Content-Type': 'application/json'},
                status=500
            )
    
    @http.route('/api/materials/<int:material_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_material_by_id(self, material_id):
        try:
            material = request.env['material.registration'].sudo().browse(material_id)
            if not material.exists():
                return json.dumps({'error': 'Material not found'})
            
            result = {
                'id': material.id,
                'material_code': material.material_code,
                'material_name': material.material_name,
                'material_type': material.material_type,
                'material_buy_price': material.material_buy_price,
                'supplier_id': material.supplier_id.id,
                'supplier_name': material.supplier_id.name,
                'create_date': material.create_date.isoformat() if material.create_date else None,
                'write_date': material.write_date.isoformat() if material.write_date else None,
            }
            
            return request.make_response(
                json.dumps({'success': True, 'data': result}),
                headers={'Content-Type': 'application/json'}
            )
            
        except Exception as e:
            return request.make_response(
                json.dumps({'error': 'Internal server error'}),
                headers={'Content-Type': 'application/json'},
                status=500
            )
