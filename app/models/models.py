from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, role_id):
        self.username = username
        self.password = password
        self.role_id = role_id

    def __repr__(self):
        return f'<User: {self.username} >'
    
class Busqueda(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buscado_por = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nombre_producto = db.Column(db.Text)
    url_img = db.Column(db.Text)
    precio_actual = db.Column(db.Text)
    precio_antes = db.Column(db.Text)
    cuotas = db.Column(db.Text)
    envio = db.Column(db.Text)
    url_ficha = db.Column(db.Text)

    def __init__(self, buscado_por, nombre_producto, url_img, precio_actual, precio_antes, cuotas, envio, url_ficha):
        self.buscado_por = buscado_por
        self.nombre_producto = nombre_producto
        self.url_img = url_img
        self.precio_actual = precio_actual
        self.precio_antes = precio_antes
        self.cuotas = cuotas
        self.envio = envio
        self.url_ficha = url_ficha

    def __repr__(self):
        return f'<Busqueda: {self.nombre_producto} >'