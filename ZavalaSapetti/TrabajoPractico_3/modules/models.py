from modules.config import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin

# Tabla de asociación para la relación muchos a muchos
asociacion_usuarios_reclamos = db.Table('usuarios_reclamos',
    Column('user_id', Integer, ForeignKey('TablaUsuarios.id'), primary_key=True),
    Column('reclamo_id', Integer, ForeignKey('TablaReclamos.id'), primary_key=True)
)

class TablaUsuarios(UserMixin, db.Model):
    __tablename__ = 'TablaUsuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    rol = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    
    # Relación uno a muchos (un usuario puede hacer varios reclamos)
    reclamos_hechos = relationship("TablaReclamos", back_populates="usuario")

    # Relación muchos a muchos (un usuario puede adherirse a varios reclamos)
    reclamos_adheridos = relationship("TablaReclamos", secondary='usuarios_reclamos', back_populates="usuarios_adheridos")

class TablaReclamos(db.Model):
    __tablename__ = 'TablaReclamos'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('TablaUsuarios.id'), nullable=False)
    asunto = Column(String(100), nullable=False)
    contenido = Column(String(1000), nullable=False)
    imagen = Column(String(255), nullable=True)
    departamento_correspondiente= Column(String(50))
    fecha = Column(Date, nullable=False)  # Usar tipo de dato Date
    estado = Column(String(20), nullable=False)  # Editable por jefe
    tiempo_de_resolucion = Column(Integer, nullable=False)  # Editable por jefe
    fecha_inicio_proceso = Column(DateTime, nullable=True)  # Nuevo atributo
    # Relación uno a muchos (un reclamo es hecho por un usuario)
    usuario = relationship("TablaUsuarios", back_populates="reclamos_hechos")

    # Relación muchos a muchos (un reclamo puede tener varios usuarios adheridos)
    usuarios_adheridos = relationship("TablaUsuarios", secondary='usuarios_reclamos', back_populates="reclamos_adheridos")
