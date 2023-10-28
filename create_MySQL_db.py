from login_db import login_db, password_db, name_server, name_db
from sqlalchemy import ForeignKey, create_engine, Table, Column, Integer, Float, String, Text
from sqlalchemy.schema import MetaData
from sqlalchemy_utils import create_database, database_exists

connection_string = f"mysql+pymysql://{login_db}:{password_db}@{name_server}"

engine = create_engine(connection_string)

with engine.connect() as connection:
    if not database_exists(connection_string + f'/{name_db}'):
        create_database(connection_string + f'/{name_db}')
    else:
        # create tables
        metadata_obj = MetaData(schema=f"{name_db}")

        products = Table(
            'products', 
            metadata_obj, 
            Column("id", Integer, primary_key = True), 
            Column("name", String(50), nullable=False), 
            Column("description", Text), 
            Column("price", Float, nullable=False)
        )     

        locations = Table(
            'locations', 
            metadata_obj, 
            Column("id", Integer, primary_key = True), 
            Column("name", String(50), nullable=False)
        )

        inventory = Table(
            'inventory',
            metadata_obj, 
            Column("id", Integer, primary_key = True), 
            Column("product_id", Integer, ForeignKey("products.id")), 
            Column('location_id', Integer, ForeignKey("locations.id")), 
            Column("quantity", Integer, nullable=False), 
        )

        #metadata_obj.drop_all(engine) # Удаление ранее созданной базы данных
        metadata_obj.create_all(engine)