from app.models.base import BaseModelMixin
from app.models.user import User
from beanie import Document, Link, BackLink
from pydantic import Json
from typing import Union, Optional, Any, List
from enum import Enum
from app.schemas.services.archieve import (
    ArchieveInputSchema,
    ArchieveOutputSchema
)

class TaskRunStatusEnum(Enum):
    QUEUED = "Queued"
    SUCCESS = "Success"
    FAILED = "Failed"
    IN_PROGRESS = "In Progress"

class WorkflowRunStatusEnum(Enum):
    SUCCESS = "Success"
    FAILED = "Failed"
    IN_PROGRESS = "In Progress"


class Task(BaseModelMixin, Document):
    user: User
    name: str
    input: Union[ArchieveInputSchema] # TODO: Add other Input Schemas of all scripts
    output: Union[ArchieveOutputSchema] # TODO: Add other Output Schemas of all scripts
    data: Optional[Json[Any]]
    parent: Optional[Link["Task"]]

    class Settings:
        collection = "task"


# TaskRun Model
class TaskRun(BaseModelMixin, Document):
    task: Optional[Link[Task]]
    input: Optional[Json[Any]]
    output: Optional[Json[Any]]
    status: TaskRunStatusEnum = TaskRunStatusEnum.QUEUED
    workflowruns: BackLink["WorkflowRun"]


# WorkFlow Model
class WorkFlow(BaseModelMixin, Document):
    user: User
    tasks: List[Link["Task"]]
    public: bool = False

    class Settings:
        collection = "workflow"


# WorkflowRun Model
class WorkflowRun(Document):
    user: User
    workflow: Link["WorkFlow"]
    tasks: List[Link["TaskRun"]]
