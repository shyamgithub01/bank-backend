from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware


from app.db.session import engine , create_engine , SessionLocal,Base
from app.routers.transactions import router as tx_router
from app.routers.accounts     import router as acc_router


app = FastAPI()


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}


app = FastAPI(title="BankX API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
def Welcome_To_Our_Bank():
    return {"message" : "welcome to our back"}
app.include_router(tx_router)

app.include_router(acc_router)


Base.metadata.create_all(bind=engine)




