from pydantic import BaseModel, Json
from typing import Union, Optional, Any, List
from beanie import Link
from app.models.task_workflow import Task, TaskRun, StatusEnum
from app.schemas.services.archieve import (
    ArchieveInputSchema,
    ArchieveOutputSchema,
)


class TaskIOSchema(BaseModel):
    name: str
    input: Union[ArchieveInputSchema]
    output: Union[ArchieveOutputSchema]
    data: Optional[Json[Any]] = None
    parent: Optional[Link["Task"]] = None
    
    
class TaskRunIOSchema(BaseModel):
    task: Optional[Link[Task]]
    input: Optional[Json[Any]]
    output: Optional[Json[Any]]
    status: StatusEnum


class WorkFlowIOSchema(BaseModel):
    tasks: List[Link["Task"]]
    public: bool = False


class WorkflowRunIOSchema(BaseModel):
    tasks: List[Link["TaskRun"]]
