from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True)
    nome = Column(String(20), nullable=False, unique=True)

    def __str__(self):
        return self.nome
    
    def __repr__(self):
        return str(self)

class Compra(Base):
    __tablename__ = 'compras'

    id = Column(Integer, primary_key=True)
    produto = Column(String(20), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    preco_medio = Column(Float, nullable=False)

    def __str__(self):
        return 'produto: {}, quantidade: {}, preço: {}, preço médio: {}'.format(self.produto, 
        self.quantidade, self.preco, self.preco_medio)
    
    def __repr__(self):
        return str(self)
    
engine = create_engine('sqlite:///estoque.db')
Base.metadata.create_all(engine)