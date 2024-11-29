from sqlalchemy import (create_engine,
                        Date, Column, Integer, String, Double, Float)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASEURL = "mysql+pymysql://root:LsantM201#@localhost/raspberry_database"

engine = create_engine(DATABASEURL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)
Base = declarative_base()


class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    descripcion = Column(String)
    precio = Column(Double)
    peso = Column(Integer)

class acelerometro(Base):
    __tablename__ = "acelerometro"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    valor_x = Column(Float)
    valor_y = Column(Float)
    valor_z = Column(Float)

class adc(Base):
    __tablename__ = "adc"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    luz_valor = Column(Float)
    voltaje = Column(Float)

class bmp(Base):
    __tablename__ = "bmp"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    temp = Column(Float)
    presion = Column(Float)
    altitud = Column(Float)

class ultrasonico(Base):
    __tablename__ = "ultrasonico"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    distancia_valor = Column(Float)