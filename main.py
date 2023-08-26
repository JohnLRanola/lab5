from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace 'your-connection-string' with your actual connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://john1:Lucban2101@35.239.116.222/john1'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    result = []
    for item in items:
        result.append({
            'id': item.id,
            'name': item.name,
            'description': item.description
        })
    return jsonify(result)

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], description=data.get('description'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created successfully'})

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404
    data = request.get_json()
    item.name = data['name']
    item.description = data.get('description')
    db.session.commit()
    return jsonify({'message': 'Item updated successfully'})

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)