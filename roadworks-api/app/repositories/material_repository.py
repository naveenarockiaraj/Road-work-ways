from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.material import Material
from app.schemas.material import MaterialCreate, MaterialUpdate


class MaterialRepository:
    def get_by_id(self, db: Session, material_id: int) -> Optional[Material]:
        return db.query(Material).filter(Material.id == material_id).first()

    def get_by_code(self, db: Session, code: str) -> Optional[Material]:
        return db.query(Material).filter(Material.material_code == code).first()

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
    ) -> Tuple[List[Material], int]:
        query = db.query(Material)
        if search:
            query = query.filter(
                or_(
                    Material.material_name.ilike(f"%{search}%"),
                    Material.material_code.ilike(f"%{search}%"),
                    Material.unit.ilike(f"%{search}%"),
                )
            )
        total = query.count()
        items = query.order_by(Material.material_name).offset(skip).limit(limit).all()
        return items, total

    def create(self, db: Session, payload: MaterialCreate) -> Material:
        material = Material(**payload.model_dump())
        db.add(material)
        db.commit()
        db.refresh(material)
        return material

    def update(self, db: Session, material: Material, payload: MaterialUpdate) -> Material:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(material, field, value)
        db.commit()
        db.refresh(material)
        return material

    def delete(self, db: Session, material: Material) -> None:
        db.delete(material)
        db.commit()


material_repository = MaterialRepository()
