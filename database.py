import os
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# DETECÇÃO DINÂMICA:
# Se o sistema operacional for Windows ('nt'), usa o banco local.
# Se for Linux (Streamlit Cloud), usa a pasta temporária /tmp/
if os.name == "nt":
    DATABASE_URL = "sqlite:///banco_setup.db"
else:
    DATABASE_URL = "sqlite:////tmp/banco_setup.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Atualizado para a versão mais recente do SQLAlchemy para sumir o aviso (Warning)
Base = declarative_base()

# 2. Criação da Tabela de Componentes
class Componente(Base):
    __tablename__ = "componentes"

    codigo = Column(String, primary_key=True, index=True) # ID Único (ex: 'COMP-123')
    tipo = Column(String, nullable=False)                  # 'Kanban' ou 'Não-Kanban'
    endereco = Column(String, nullable=True)              # 'Corredor A, Prateleira 2' ou 'Linha'
    data_cadastro = Column(DateTime, default=datetime.now) # Data automática do cadastro

# 3. Função para inicializar o banco (CORRIGIDA: de create_create_all para create_all)
def inicializar_banco():
    Base.metadata.create_all(bind=engine)

# 4. Função auxiliar para obter uma sessão com o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    # Se você rodar este arquivo diretamente, ele cria o banco de dados para testar
    inicializar_banco()
    print("Banco de dados e tabela 'componentes' criados com sucesso!")