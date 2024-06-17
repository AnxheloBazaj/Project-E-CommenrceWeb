from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Product:
    db_name = "e-commerce.shcema"

    def __init__(self, data):
        self.id = data["id"]
        self.product_name = data["product_name"]
        self.description = data["description"]
        self.price = data["price"]
        self.stock_quantity = data["stock_quantity"]
        self.image = data["image"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.category_id = data["category_id"]

    @classmethod
    def get_all_Products(cls):
        query = "SELECT * FROM products LEFT JOIN categories ON products.category_id = categories.category_id;"
        result = connectToMySQL(cls.db_name).query_db(query)
        products = []
        if result:
            for product in result:
                products.append(product)
            return products

    @classmethod
    def createCategory(cls, data):
        query = "INSERT INTO categories (category_name) VALUES(%(category_name)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def getCategories(cls):
        query = "SELECT * FROM categories;"
        result = connectToMySQL(cls.db_name).query_db(query)
        categories = []
        if result:
            for category in result:
                categories.append(category)
            return categories


    @classmethod
    def create(cls, data):
        query = "INSERT INTO products (product_name, description, price, stock_quantity,image, category_id) VALUES(%(product_name)s, %(description)s, %(price)s,%(stock_quantity)s,%(image)s,%(category_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_product(cls, data):
        query = "UPDATE products SET description = %(description)s, price=%(price)s, stock_quantity = %(stock_quantity)s, image = %(image)s  WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_product(cls, data):
        query = "DELETE FROM products WHERE id = %(product_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_product_by_id(cls, data):
        query = "SELECT * FROM products left join categories on products.category_id = categories.category_id WHERE products.id = %(product_id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
    @classmethod
    def get_product_by_category(cls, data):
        query = "SELECT * FROM products WHERE category_id = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        products = []
        if result:
            for product in result:
                products.append(product)
            return products

    @classmethod
    def delete_categorys_products(cls, data):
        query = "DELETE FROM products WHERE products.category_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_product(data):
        is_valid = True
        # test whether a field matches the pattern
        if len(data["product_name"]) < 3:
            flash("Products name should be at least 3 characters!", "productName")
            is_valid = False
        if not data["price"]:
            flash("Price is required!", "price")
            is_valid = False
        else:
            try:
                price = int(data["price"])
                if price <= 0:
                    flash("Price must be bigger than zero!", "price")
                    is_valid = False
            except ValueError:
                flash("Price must be a valid integer!", "price")
                is_valid = False
        if not data["stock_quantity"]:
            flash("Stock quantity is required!", "stockQuantity")
            is_valid = False
        else:
            try:
                stock_quantity = int(data["stock_quantity"])
                if stock_quantity <= 0:
                    flash("Can't add an item for sale if the quantity is zero or less!", "stockQuantity")
                    is_valid = False
            except ValueError:
                flash("Stock quantity must be a valid integer!", "stockQuantity")
                is_valid = False
        # if not data["image_url"]:
        #     flash("The image of the product is required!", "productImage")
        #     is_valid = False
        if len(data["description"]) < 3:
            flash("Description should be at least 3 characters!", "description")
            is_valid = False
        return is_valid
