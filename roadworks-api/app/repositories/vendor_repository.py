from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate


class VendorRepository:
    def get_by_id(self, db: Session, vendor_id: int) -> Optional[Vendor]:
        return db.query(Vendor).filter(Vendor.id == vendor_id).first()

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
    ) -> Tuple[List[Vendor], int]:
        query = db.query(Vendor)
        if search:
            query = query.filter(
                or_(
                    Vendor.vendor_name.ilike(f"%{search}%"),
                    Vendor.contact_person.ilike(f"%{search}%"),
                    Vendor.mobile_number.ilike(f"%{search}%"),
                    Vendor.gst_number.ilike(f"%{search}%"),
                )
            )
        total = query.count()
        items = query.order_by(Vendor.vendor_name).offset(skip).limit(limit).all()
        return items, total

    def create(self, db: Session, payload: VendorCreate) -> Vendor:
        vendor = Vendor(**payload.model_dump())
        db.add(vendor)
        db.commit()
        db.refresh(vendor)
        return vendor

    def update(self, db: Session, vendor: Vendor, payload: VendorUpdate) -> Vendor:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(vendor, field, value)
        db.commit()
        db.refresh(vendor)
        return vendor

    def delete(self, db: Session, vendor: Vendor) -> None:
        db.delete(vendor)
        db.commit()


vendor_repository = VendorRepository()
