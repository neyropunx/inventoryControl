from login_db import db, app
from flask import redirect, render_template, request
from sqlalchemy.sql import text
from sqlalchemy import func
import re 


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)

    product_id = db.relationship("Inventory", backref="product")

    def __repr__(self):
        return f"<product {self.id} {self.name}>"
    
class Locations(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    location_id = db.relationship("Inventory", backref="location")

    def __repr__(self):
        return f"<location {self.id} {self.name}>"
    
class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<inventory {self.id}>"
    
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/index')
def main():
    products = db.session.query(Products.id, Products.name, Products.description, Products.price,
                           func.group_concat(Locations.name).label('locations'), 
                           func.group_concat(Inventory.quantity).label('quantity'),
                           func.group_concat(Inventory.id).label('inventory')).join(Products).join(Locations).group_by(Products.id)
    locations = db.session.query(Locations).all()
    return render_template("index.html", products=products, locations=locations)

@app.get('/_table')
def showTable():
    products = db.session.query(Products.id, Products.name, Products.description, Products.price,
                           func.group_concat(Locations.name).label('locations'), 
                           func.group_concat(Inventory.quantity).label('quantity'),
                           func.group_concat(Inventory.id).label('inventory')).join(Products).join(Locations).group_by(Products.id)
    return render_template("_table.html", products=products)

@app.get('/_search_product')
def search_product():
    '''
        Поиск по названию товара

        product_name - наименование товара, получаемое из GET запроса скрипта search_product
        invetorys - запрос из БД с фильтрацией по id в таблице Inventory

        Возвращает код страницы с запрашиваемыми товарами
    '''

    product_name = request.args.get('product_name').lower()
    products = db.session.query(Products.id, Products.name, Products.description, Products.price,
                        func.group_concat(Locations.name).label('locations'), 
                        func.group_concat(Inventory.quantity).label('quantity'),
                        func.group_concat(Inventory.id).label('inventory')).join(Products).join(Locations).group_by(Products.id)
    products = products.filter(Products.name.contains(product_name))
    return render_template("_table.html", products=products)

@app.get('/_search_location')
def search_location():
    '''
        Поиск по названию товара

        product_name - наименование товара, получаемое из AJAX GET запроса скрипта search_location
        invetorys - запрос из БД с фильтрацией по id в таблице Inventory

        Возвращает код страницы с запрашиваемыми товарами
    '''
    try:
        locations = request.args.get('location')
        locations = [int(i) for i in re.findall(r'\d*\.\d+|\d+', locations)]
        print(locations)   
        products = db.session.query(Products.id, Products.name, Products.description, Products.price,
                            func.group_concat(Locations.name).label('locations'), 
                            func.group_concat(Inventory.quantity).label('quantity'),
                            func.group_concat(Inventory.id).label('inventory')).join(Products).join(Locations).group_by(Products.id)
        if len(locations) > 0:
            products = products.filter(Inventory.location_id.in_(locations))
        print(products)
        return render_template("_table.html", products=products)
    except:
        return 'Ошибка поиска по локации'

@app.route('/_append_product', methods=['GET', 'POST'])
def append_product():
    '''
        Добавление нового товара

        Данные приходят из скрипта append_product
    '''

    if request.method == 'GET':
        locations = db.session.query(Locations).all()
        return render_template("_append_product.html", locations=locations)
    if request.method == 'POST':
        try:        
            data = request.get_json()
            product_name = data['product_name']
            product_description = data['product_description']
            product_price = int(data['product_price'])
            product = Products(name=product_name, description=product_description, price=product_price)
            db.session.add(product)
            db.session.flush()
            
            location_id = int(data['location_id'])
            quantity = int(data['quantity'])
            inventory = Inventory(product_id=product.id, location_id=location_id, quantity=quantity)
            db.session.add(inventory)
            db.session.commit()
            return 'Добавлен'
        except:
            db.session.rollback()
            return 'Ошибка добавления в БД'

@app.route('/_append_location', methods=['GET', 'POST'])
def append_location():
    '''
        Добавление новой локации

        Данные приходят из скрипта append_location
    '''
    if request.method == 'GET':
        locations = db.session.query(Locations).all()
        return render_template("_append_location.html", locations=locations)
    if request.method == 'POST':
        try:
            location_name = request.get_data(as_text=True)
            location = Locations(name=location_name)
            db.session.add(location)
            db.session.commit()
            return 'Добавлено'
        except:
            db.session.rollback()
            print('append error')
            return "Ошибка добавления в БД"
        
@app.route('/_remove_location', methods=['GET', 'POST'])
def remove_location():
    '''
        Удаление локации

        Данные приходят из скрипта remove_location
    '''
    if request.method == 'GET':
        locations = db.session.query(Locations).all()
        return render_template("_append_location.html", locations=locations)
    if request.method == 'POST':
        try:
            location_id = request.get_data(as_text=True)
            location = db.session.query(Locations).get_or_404(int(location_id))
            db.session.delete(location)
            db.session.commit()
            return 'Удалено'
        except:
            db.session.rollback()
            print('remove error')
            return "Ошибка удаления из БД"

@app.route('/_append_inventory', methods=['GET', 'POST'])
def append_inventory():
    '''
        Добавление товара на склад

        Данные приходят из скрипта append_inventory
    '''

    if request.method == 'GET':
        product_id = request.args.get('product_id')
        product = db.session.query(Products.id, Products.name, Products.description, Products.price,
                    func.group_concat(Locations.name).label('locations_name'), 
                    func.group_concat(Inventory.quantity).label('quantity'),
                    func.group_concat(Inventory.id).label('inventory_id')).join(Products).join(Locations).group_by(Products.id)
        product = product.filter(Products.id == product_id)
        locations = db.session.query(Locations).all()
        return render_template('_append_inventory.html', product=product, locations=locations)
    
    if request.method == 'POST':
        data = request.get_json()
        product_id = data['product_id']
        location_id = data['location_id']
        quantity = data['quantity']
        if db.session.query(Inventory) \
                    .filter(Inventory.product_id == product_id) \
                    .filter(Inventory.location_id == location_id).all():
            try:    
                statement = text('update inventory \
                                set quantity = inventory.quantity + :quantity \
                                where product_id = :product_id and location_id = :location_id')
                db.session.execute(statement, {'product_id':product_id,
                                            'location_id':location_id, 
                                            'quantity':quantity})
                db.session.commit()
                return 'Добавлено'
            except:
                print('update error')
                db.session.rollback()
                return 'Ошибка добавления на склад (append)'
        elif db.session.query(Inventory) \
                    .filter(Inventory.product_id == product_id) \
                    .filter(Inventory.location_id != location_id).all():
            try:    
                statement = text('insert into inventory (product_id, location_id, quantity) \
                                 values (:product_id, :location_id, :quantity)')
                db.session.execute(statement, {'product_id':product_id,
                                               'location_id':location_id, 
                                               'quantity':quantity})
                db.session.commit()
                return 'Добавлено'
            except:
                print('update error')
                db.session.rollback()
                return 'Ошибка добавления на склад (new)'
            
    return redirect('/')
    
@app.route('/_remove_inventory', methods=['GET', 'POST'])
def remove_inventory():
    '''
        Удаление товара со склада

        Данные приходят из скрипта remove_inventory
    '''
    if request.method == 'GET':
        product_id = request.args.get('product_id')
        product = db.session.query(Products.id, Products.name, Products.description, Products.price,
                    func.group_concat(Locations.name).label('locations_name'),
                    func.group_concat(Locations.id).label('locations_id'),  
                    func.group_concat(Inventory.quantity).label('quantity'),
                    func.group_concat(Inventory.id).label('inventory_id')).join(Products).join(Locations).group_by(Products.id)
        product = product.filter(Products.id == product_id)

        statement = text('select locations.* \
                    from inventory \
                    join products on inventory.product_id = products.id \
                    join locations on inventory.location_id = locations.id \
                    where inventory.product_id = :product_id')
        locations = db.session.execute(statement, {'product_id':product_id}).all()
        return render_template('_append_inventory.html', product=product, locations=locations)
        
    if request.method == 'POST':
        data = request.get_json()
        product_id = data['product_id']
        location_id = data['location_id']
        quantity = data['quantity']
        inventory = db.session.query(Inventory) \
                    .filter(Inventory.product_id == product_id) \
                    .filter(Inventory.location_id == location_id) \
                    .filter(Inventory.quantity > quantity).first()
        if inventory:
            try:
                statement = text('update inventory \
                                set quantity = inventory.quantity - :quantity \
                                where product_id = :product_id and location_id = :location_id')
                db.session.execute(statement, {'product_id':product_id,
                                            'location_id':location_id, 
                                            'quantity':quantity})
                db.session.commit()
                return 'Удалено со склада'
            except:
                print('update error')
                db.session.rollback()
                return 'Ошибка удаления товара со склада'
        else:
            return 'Недостаточно товара на складе'
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)