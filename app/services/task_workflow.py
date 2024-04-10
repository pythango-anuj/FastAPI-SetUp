from app.models.task_workflow import (
    Task, 
    TaskRun, 
    WorkFlow,
    WorkflowRun
)
from app.schemas.task_workflow import (
    TaskIOSchema,
    TaskRunIOSchema,
    WorkFlowIOSchema,
    WorkflowRunIOSchema
)
from app.utils.exceptions import AppException
from app.services.base import BaseService, BaseCRUD
from app.utils.result import ServiceResult

# Task Service
class TaskService(BaseService):
    def create_item(self, task: TaskIOSchema) -> ServiceResult:
        task_item = TaskCRUD(self.db).create_item(task)
        if not task_item:
            return ServiceResult(AppException.CreateItem())
        return ServiceResult(task_item)

    def get_item(self, task_id: int) -> ServiceResult:
        task_item = TaskCRUD(self.db).get_item(task_id)
        if not task_item:
            return ServiceResult(AppException.GetItem({"task_id": task_id}))
        return ServiceResult(task_item)


class TaskCRUD(BaseCRUD):
    def create_item(self, task: TaskIOSchema) -> TaskIOSchema:
        task_item = Task(**task)
        self.db.add(task_item)
        self.db.commit()
        self.db.refresh(task_item)
        return task_item

    def get_item(self, task_id: int) -> TaskIOSchema:
        task_item = self.db.query(Task).filter(Task.id == task_id).first()
        if task_item:
            return task_item
        return None


# TaskRun Service
class TaskRunService(BaseService):
    def create_item(self, user_task: TaskRunIOSchema) -> ServiceResult:
        user_task_item = TaskRunCRUD(self.db).create_item(user_task)
        if not user_task_item:
            return ServiceResult(AppException.CreateItem())
        return ServiceResult(user_task_item)

    def get_item(self, user_task_id: int) -> ServiceResult:
        user_task_item = TaskRunCRUD(self.db).get_item(user_task_id)
        if not user_task_item:
            return ServiceResult(AppException.GetItem({"user_task_id": user_task_id}))
        return ServiceResult(user_task_item)


class TaskRunCRUD(BaseCRUD):
    def create_item(self, user_task: TaskRunIOSchema) -> TaskRunIOSchema:
        user_task_item = TaskRun(**user_task)
        self.db.add(user_task_item)
        self.db.commit()
        self.db.refresh(user_task_item)
        return user_task_item

    def get_item(self, user_task_id: int) -> TaskRunIOSchema:
        user_task_item = self.db.query(TaskRun).filter(TaskRun.id == user_task_id).first()
        if user_task_item:
            return user_task_item
        return None
    
# Workflow Service
class WorkFlowService(BaseService):
    def create_item(self, workflow: WorkFlowIOSchema) -> ServiceResult:
        workflow_item = WorkFlowCRUD(self.db).create_item(workflow)
        if not workflow_item:
            return ServiceResult(AppException.CreateItem())
        return ServiceResult(workflow_item)

    def get_item(self, workflow_id: int) -> ServiceResult:
        workflow_item = WorkFlowCRUD(self.db).get_item(workflow_id)
        if not workflow_item:
            return ServiceResult(AppException.GetItem({"workflow_id": workflow_id}))
        if not workflow_item.public:
            return ServiceResult(AppException.ItemRequiresAuth())
        return ServiceResult(workflow_item)


class WorkFlowCRUD(BaseCRUD):
    def create_item(self, workflow: WorkFlowIOSchema) -> WorkFlowIOSchema:
        workflow_item = WorkFlow(**workflow)
        self.db.add(workflow_item)
        self.db.commit()
        self.db.refresh(workflow_item)
        return workflow_item

    def get_item(self, workflow_id: int) -> WorkFlowIOSchema:
        workflow_item = self.db.query(WorkFlow).filter(WorkFlow.id == workflow_id).first()
        if workflow_item:
            return workflow_item
        return None


# WorkFLowRun Service
class WorkflowRunService(BaseService):
    def create_item(self, workflow_run: WorkflowRunIOSchema) -> ServiceResult:
        workflow_run_item = WorkflowRunCRUD(self.db).create_item(workflow_run)
        if not workflow_run_item:
            return ServiceResult(AppException.CreateItem())
        return ServiceResult(workflow_run_item)

    def get_item(self, workflow_run_id: int) -> ServiceResult:
        workflow_run_item = WorkflowRunCRUD(self.db).get_item(workflow_run_id)
        if not workflow_run_item:
            return ServiceResult(AppException.GetItem({"workflow_run_id": workflow_run_id}))
        return ServiceResult(workflow_run_item)


class WorkflowRunCRUD(BaseCRUD):
    def create_item(self, user_task: WorkflowRunIOSchema) -> WorkflowRunIOSchema:
        workflow_run_item = WorkflowRun(**user_task)
        self.db.add(workflow_run_item)
        self.db.commit()
        self.db.refresh(workflow_run_item)
        return workflow_run_item

    def get_item(self, workflow_run_id: int) -> WorkflowRunIOSchema:
        workflow_run_item = self.db.query(WorkflowRun).filter(WorkflowRun.id == workflow_run_id).first()
        if workflow_run_item:
            return workflow_run_item
        return None