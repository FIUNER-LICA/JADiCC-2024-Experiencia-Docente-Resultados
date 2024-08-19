# models.py contiene todas las clases usadas para modelar las tablas de la base de datos
from modules.config import db
from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey 
from flask_login import UserMixin
from sqlalchemy.orm import relationship


asociacion_usuarios_reclamos = db.Table('usuarios_reclamos',
    Column('usuario_id', Integer, ForeignKey('Usuarios.id')),
    Column('reclamo_id', Integer, ForeignKey('Reclamos.id'))
)

class Usuario(db.Model , UserMixin):
    __tablename__ = 'Usuarios'
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    claustro = Column(String(20), nullable=False)
    rol = Column(String(20), nullable=False)
    nombre_de_usuario = Column(String(20), nullable=False, unique = True)
    email = Column(String(100), nullable=False, unique = True)
    password = Column (db.String (20))
    reclamos = relationship("Reclamo", secondary='usuarios_reclamos', backref="usuarios")
   
class Reclamo(db.Model):
    __tablename__ = 'Reclamos'
    id = Column(Integer(), primary_key=True)
    usuario_id = Column(Integer, ForeignKey("Usuarios.id"))
    asunto = Column(String(100), nullable=False)
    nombre_imagen = Column(String(50), nullable=False)
    contenido = Column(String(2000), nullable=False)
    departamento_correspondiente = Column(String(50), nullable=False)
    fecha_y_hora = Column(String(15), nullable=False)
    estado = Column(String(15), nullable=False)
    numero_adheridos = Column(Integer())
    

class Departamento(db.Model):
    __tablename__ = 'Departamentos'
    id = Column(Integer(), primary_key=True)
    nombre_departamento = Column(String(50), nullable=False)
    usuario_jefe_id = Column(Integer, nullable=False)
    






# No es necesaria la tabla de Departamento
# class Departamento_DB(db.Model):
    # __tablename__ = 'DepartamentoS_DB'
    # id = Column(Integer(), primary_key=True)
    # id_reclamos = Column(ARRAY (Integer), nullable=False)


# db.Model es una clase base de SQLAlchemy que se utiliza para definir modelos
# de datos en una aplicación Flask. 
# Esta clase proporciona una interfaz para interactuar con la base de datos utilizando 
# objetos Python que representan las tablas y columnas de la base de datos.

# __tablename__ corresponde al nombre de la tabla SQL dentro de la base de datos

# primary_key es un campo o conjunto de campos que identifica de manera única cada
# registro en una tabla. suele ser un campo numérico autoincremental que no permite 
# valores duplicados y que se utiliza como índice para acceder a los registros 
# de la tabla de forma rápida y eficiente