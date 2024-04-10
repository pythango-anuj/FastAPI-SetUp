from fastapi import FastAPI, Depends
from pydantic import BaseModel
from app.config.env import KAFKA_BROKER_URL
from faststream.kafka.fastapi import KafkaRouter
from app.config.database import init_db
from contextlib import asynccontextmanager

router = KafkaRouter(KAFKA_BROKER_URL)

kafka_lifespan = router.lifespan_context

@asynccontextmanager
async def lifespan_wrapper(app):
    print("App Started->->")
    await init_db()
    async with kafka_lifespan(app) as maybe_state:
        yield maybe_state
    print("App Closed <-<-")

lifespan = lifespan_wrapper


app = FastAPI(lifespan=lifespan)



app.include_router(router)
    

class Incoming(BaseModel):
    m: dict


def call():
    return True


@router.subscriber("test")
@router.publisher("response")
async def hello(m: Incoming, d=Depends(call)):
    return {"response": "Hello, world!"}