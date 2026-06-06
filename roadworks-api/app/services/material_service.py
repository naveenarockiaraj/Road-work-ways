from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ConflictException
from app.repositories.material_repository import material_repository
from app.schemas.material import MaterialCreate, MaterialUpdate, MaterialResponse
from typing import Optional
from app.utils.pagination import PaginatedResponse, PaginationParams


class MaterialService:
    def list_materials(
        self, db: Session, params: PaginationParams, search: Optional[str] = None
    ) -> PaginatedResponse[MaterialResponse]:
        items, total = material_repository.get_all(
            db, skip=params.skip, limit=params.limit, search=search
        )
        return PaginatedResponse(
            items=[MaterialResponse.model_validate(m) for m in items],
            total=total,
            page=params.page,
            size=params.limit,
        )

    def get_material(self, db: Session, material_id: int) -> MaterialResponse:
        material = material_repository.get_by_id(db, material_id)
        if not material:
            raise NotFoundException("Material", str(material_id))
        return MaterialResponse.model_validate(material)

    def create_material(self, db: Session, payload: MaterialCreate) -> MaterialResponse:
        if material_repository.get_by_code(db, payload.material_code):
            raise ConflictException(f"Material with code '{payload.material_code}' already exists")
        material = material_repository.create(db, payload)
        return MaterialResponse.model_validate(material)

    def update_material(
        self, db: Session, material_id: int, payload: MaterialUpdate
    ) -> MaterialResponse:
        material = material_repository.get_by_id(db, material_id)
        if not material:
            raise NotFoundException("Material", str(material_id))
        material = material_repository.update(db, material, payload)
        return MaterialResponse.model_validate(material)

    def delete_material(self, db: Session, material_id: int) -> None:
        material = material_repository.get_by_id(db, material_id)
        if not material:
            raise NotFoundException("Material", str(material_id))
        material_repository.delete(db, material)


material_service = MaterialService()
