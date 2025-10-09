from fastapi import FastAPI
from database import engine, Base
import models
from routers import titulares, dispositivos, finalidades, tipos_dados, opcoes_tratamento, consentimentos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Módulo de Gerenciamento de Consentimento",
    description="API para gerenciar o consentimento de titulares de dados em um ecossistema IoT, conforme a LGPD.",
    version="0.1.0"
)

# Inclui os routers
app.include_router(titulares.router)
app.include_router(dispositivos.router)
app.include_router(finalidades.router)
app.include_router(tipos_dados.router)
app.include_router(opcoes_tratamento.router)
app.include_router(consentimentos.router)

# Rota de teste para verificar se a API está funcionando
@app.get("/")
def read_root():
    return {"status": "API do MGC está online!"}

# Rota para testar a saúde da conexão com o banco de dados
@app.get("/healthcheck")
def health_check():
    try:
        # Tenta criar uma conexão simples para verificar se o banco está acessível
        connection = engine.connect()
        connection.close()
        return {"status": "ok", "database": "conectado"}
    except Exception as e:
        return {"status": "error", "database": "desconectado", "details": str(e)}