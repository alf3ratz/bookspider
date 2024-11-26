# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import psycopg2
from psycopg2 import sql



class BookvoedPipeline:
    def __init__(self):
        db_name = os.getenv('db_name')
        db_user = os.getenv('db_user')
        db_pswd = os.getenv('db_pswd')
        db_host = os.getenv('db_host')
        self.conn = psycopg2.connect(database=db_name, user=db_user,
                                     password=db_pswd, host=db_host, port=6432)
        cursor = self.conn.cursor()
        cursor.execute("""
            create table if not exists books (
                id serial PRIMARY KEY,
                name VARCHAR(255),
                author VARCHAR(255),
                price VARCHAR(255)             
            )
        """)
        self.connection.commit()

    def process_item(self, item, spider):
        if 'error' in item:
            print('Can\'t add error item to database')
            return item

        cursor = self.connection.cursor()
        name = item['name']
        author = item['author']
        price = item['price']
        cursor.execute(f'INSERT INTO items (name, author, price) VALUES ({name}, {author}, {price})')
        self.connection.commit()

        return item
