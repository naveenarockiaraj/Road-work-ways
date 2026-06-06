from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ConflictException
from app.repositories.project_repository import project_repository
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.models.project import ProjectStatus
from typing import Optional
from app.utils.pagination import PaginatedResponse, PaginationParams


class ProjectService:
    def list_projects(
        self,
        db: Session,
        params: PaginationParams,
        search: Optional[str] = None,
        status: Optional[ProjectStatus] = None,
    ) -> PaginatedResponse[ProjectResponse]:
        items, total = project_repository.get_all(
            db, skip=params.skip, limit=params.limit, search=search, status=status
        )
        return PaginatedResponse(
            items=[ProjectResponse.model_validate(p) for p in items],
            total=total,
            page=params.page,
            size=params.limit,
        )

    def get_project(self, db: Session, project_id: int) -> ProjectResponse:
        project = project_repository.get_by_id(db, project_id)
        if not project:
            raise NotFoundException("Project", str(project_id))
        return ProjectResponse.model_validate(project)

    def create_project(self, db: Session, payload: ProjectCreate) -> ProjectResponse:
        if project_repository.get_by_code(db, payload.project_code):
            raise ConflictException(f"Project with code '{payload.project_code}' already exists")
        project = project_repository.create(db, payload)
        return ProjectResponse.model_validate(project)

    def update_project(
        self, db: Session, project_id: int, payload: ProjectUpdate
    ) -> ProjectResponse:
        project = project_repository.get_by_id(db, project_id)
        if not project:
            raise NotFoundException("Project", str(project_id))
        project = project_repository.update(db, project, payload)
        return ProjectResponse.model_validate(project)

    def delete_project(self, db: Session, project_id: int) -> None:
        project = project_repository.get_by_id(db, project_id)
        if not project:
            raise NotFoundException("Project", str(project_id))
        project_repository.delete(db, project)


project_service = ProjectService()
