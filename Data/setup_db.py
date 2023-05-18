import sqlite3
from sqlite3 import Error

database = r"./Data/database.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

##### CREATE TABLES ######## 


sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER UNIQUE NOT NULL,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL,
                                PRIMARY KEY(user_id)
                            );"""

sql_create_items_table = """CREATE TABLE IF NOT EXISTS items (
                                item_id INTEGER UNIQUE NOT NULL,
                                title TEXT NOT NULL,
                                description TEXT NOT NULL,
                                price REAL NOT NULL,
                                owner_id TEXT NOT NULL,

                                -- Parameters for selecting etc.
                                size TEXT,
                                stock INT,

                                PRIMARY KEY(item_id),
                                FOREIGN KEY(owner_id) REFERENCES users(user_id)
                            );"""

sql_create_orders_table = """CREATE TABLE IF NOT EXISTS orders (
                                order_id INTEGER UNIQUE NOT NULL,
                                order_date DATE NOT NULL,
                                user_id INTEGER NOT NULL,
                                product_id INTEGER NOT NULL,
                                -- Other important features for the order table
                                quantity INTEGER NOT NULL,
                                total_amount REAL NOT NULL,

                                PRIMARY KEY(order_id),
                                FOREIGN KEY(user_id) REFERENCES users(user_id),
                                FOREIGN KEY(product_id) REFERENCES items(item_id)
                            );"""

sql_create_images_table = """CREATE TABLE IF NOT EXISTS images (
                                path TEXT NOT NULL,
                                displayOrder INT NOT NULL,
                                product_id INTEGER NOT NULL,
                                FOREIGN KEY(product_id) REFERENCES items(item_id)
                            );"""

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

#### INSERT #########

def add_user(conn, user_id, username, password):
    """ Add a new user into the users table
    :param conn:
    :param user_id:
    :param username:
    :param password:
    """
    sql = ''' INSERT INTO users(user_id, username, password)
              VALUES(?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (user_id, username, password))
        conn.commit()
    except Error as e:
        print(e)

def init_users(conn):
    init = [(969001, "elza", "pbkdf2:sha256:260000$l4XlAvApLYlgJTpe$3519a342c351d894f2a60ee0f54fadb41d383682ec3be86587fae7e0afd4e3ad")]
    for u in init:
        add_user(conn, u[0], u[1], u[2])


def add_item(conn, item_id, title, description, price, owner_id):
    """ Add a new item into the items table
    :param conn:
    :param item_id:
    :param title:
    :param description:
    :param price:
    :param owner_id:
    """
    sql = ''' INSERT INTO items(item_id, title, description, price, owner_id)
              VALUES(?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (item_id, title, description, price, owner_id))
        conn.commit()
    except Error as e:
        print(e)

def init_items(conn):
    init = [(1, "Sofa", "En fin sofa", 1000, 111111),
            (2, "Stol", "En fin stol", 500, 222222),
            (3, "Bord", "Et fint bord", 2000, 333333)]
    for i in init:
        add_item(conn, i[0], i[1], i[2], i[3], i[4])


def add_order(conn, order_id, order_date, user_id, product_id, quantity, total_amount):
    """
    Add a new order into the orders table
    :param conn: SQLite connection object
    :param order_id: Order ID
    :param order_date: Order date
    :param user_id: User ID associated with the order
    :param product_id: Product ID associated with the order
    :param quantity: Quantity of the product in the order
    :param total_amount: Total amount of the order
    """
    sql = ''' INSERT INTO orders(order_id, order_date, user_id, product_id, quantity, total_amount)
              VALUES(?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (order_id, order_date, user_id, product_id, quantity, total_amount))
        conn.commit()
    except Error as e:
        print(e)

def init_orders(conn):
    init = [(1, '2023-05-01', 969001, 1, 1, 299.99),
            (2, '2023-05-02', 969001, 2, 2, 149.99),
            (3, '2023-05-03', 969001, 3, 3, 179.99)]
    for o in init:
        add_order(conn, o[0], o[1], o[2], o[3], o[4], o[5])


def add_image(conn, path, displayOrder, product_id):
    """ Add a new image into the images table
    :param conn:
    :param path:
    :param displayOrder:
    :param product_id:
    """
    sql = ''' INSERT INTO images(path, displayOrder, product_id) 
              VALUES(?, ?, ?)'''
    
    try:
        cur = conn.cursor()
        cur.execute(sql, (path, displayOrder, product_id))
        conn.commit()
    except Error as e:
        print(e)

def init_images(conn):
    path = "/static/Images/ProductImages/"
    init = [(path + "sofa.jpg",   1, 1),
            (path + "sofa2.jpeg", 2, 1),
            (path + "stol.jpg",   1, 2),
            (path + "sofa3.jpg",  3, 1),
            (path + "bord.jpg",   1, 3)]
    for i in init:
        add_image(conn, i[0], i[1], i[2])

def alter_table(conn, bio, address, phone, user_id):
    try:
        c = conn.cursor()
        c.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in c.fetchall()]

        if 'bio' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN bio TEXT;")
        if 'address' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN address TEXT;")
        if 'phone' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN phone INTEGER;")


        c.execute("UPDATE users SET bio = ?, address = ?, phone = ? WHERE user_id = ?",
                  (bio, address, phone, user_id))
        
        conn.commit()
    except Error as e:
        print(e)

def init_usercontent(conn):
    init = [('Happy', 'In the clouds <3', 42015210, 969001)]
    for i in init:
        alter_table(conn, i[0], i[1], i[2], i[3])


#### SETUP ####

def setup():
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_items_table)
        create_table(conn, sql_create_orders_table)
        create_table(conn, sql_create_images_table)
        init_users(conn)
        init_items(conn)
        init_orders(conn)
        init_images(conn)
        init_usercontent(conn)

        conn.close()


if __name__ == '__main__':
    # If executed as main, this will create tables and insert initial data
    setup()