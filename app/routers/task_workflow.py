from fastapi import APIRouter, Depends
from app.services.task_workflow import TaskService, WorkFlowService
from app.schemas.task_workflow import TaskIOSchema, WorkFlowIOSchema
from app.utils.result import handle_result
from app.config.database import get_db

router = APIRouter(
    tags=["Tasks and Workflows"],
    responses={404: {"description": "Not found"}},
)


@router.post("/task/", response_model=TaskIOSchema)
async def create_item(task: TaskIOSchema, db: get_db = Depends()):
    result = TaskService(db).create_item(task)
    return handle_result(result)


@router.get("/task/{task_id}/", response_model=TaskIOSchema)
async def get_item(task_id: int, db: get_db = Depends()):
    result = TaskService(db).get_item(task_id)
    return handle_result(result)

@router.post("/workflow/", response_model=WorkFlowIOSchema)
async def create_item(workflow: WorkFlowIOSchema, db: get_db = Depends()):
    result = WorkFlowService(db).create_item(workflow)
    return handle_result(result)


@router.get("/workflow/{workflow_id}/", response_model=WorkFlowIOSchema)
async def get_item(workflow_id: int, db: get_db = Depends()):
    result = WorkFlowService(db).get_item(workflow_id)
    return handle_result(result)