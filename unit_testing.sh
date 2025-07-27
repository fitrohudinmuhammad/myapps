curl -X GET "http://localhost:8069/api/materials"

curl -X GET "http://localhost:8069/api/materials?material_type=fabric"

curl -X POST "http://localhost:8069/api/materials" \
  -d '{
    "material_code": "MAT001",
    "material_name": "Premium Cotton",
    "material_type": "cotton",
    "material_buy_price": 150.0,
    "supplier_id": 1
  }'

curl -X PUT "http://localhost:8069/api/materials/1" \
  -d '{
    "material_buy_price": 175.0
  }'

curl -X DELETE "http://localhost:8069/api/materials/1"
