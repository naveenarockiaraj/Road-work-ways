from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.project import Project, ProjectStatus
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def get_by_id(self, db: Session, project_id: int) -> Optional[Project]:
        return db.query(Project).filter(Project.id == project_id).first()

    def get_by_code(self, db: Session, code: str) -> Optional[Project]:
        return db.query(Project).filter(Project.project_code == code).first()

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        status: Optional[ProjectStatus] = None,
    ) -> Tuple[List[Project], int]:
        query = db.query(Project)
        if search:
            query = query.filter(
                or_(
                    Project.project_name.ilike(f"%{search}%"),
                    Project.project_code.ilike(f"%{search}%"),
                    Project.district.ilike(f"%{search}%"),
                )
            )
        if status:
            query = query.filter(Project.status == status)
        total = query.count()
        items = query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
        return items, total

    def create(self, db: Session, payload: ProjectCreate) -> Project:
        project = Project(**payload.model_dump())
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    def update(self, db: Session, project: Project, payload: ProjectUpdate) -> Project:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        db.commit()
        db.refresh(project)
        return project

    def delete(self, db: Session, project: Project) -> None:
        db.delete(project)
        db.commit()

    def count_active(self, db: Session) -> int:
        return db.query(Project).filter(Project.status == ProjectStatus.IN_PROGRESS).count()

    def count_total(self, db: Session) -> int:
        return db.query(Project).count()


project_repository = ProjectRepository()
