from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from app.repositories.vendor_repository import vendor_repository
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse
from typing import Optional
from app.utils.pagination import PaginatedResponse, PaginationParams


class VendorService:
    def list_vendors(
        self, db: Session, params: PaginationParams, search: Optional[str] = None
    ) -> PaginatedResponse[VendorResponse]:
        items, total = vendor_repository.get_all(
            db, skip=params.skip, limit=params.limit, search=search
        )
        return PaginatedResponse(
            items=[VendorResponse.model_validate(v) for v in items],
            total=total,
            page=params.page,
            size=params.limit,
        )

    def get_vendor(self, db: Session, vendor_id: int) -> VendorResponse:
        vendor = vendor_repository.get_by_id(db, vendor_id)
        if not vendor:
            raise NotFoundException("Vendor", str(vendor_id))
        return VendorResponse.model_validate(vendor)

    def create_vendor(self, db: Session, payload: VendorCreate) -> VendorResponse:
        vendor = vendor_repository.create(db, payload)
        return VendorResponse.model_validate(vendor)

    def update_vendor(
        self, db: Session, vendor_id: int, payload: VendorUpdate
    ) -> VendorResponse:
        vendor = vendor_repository.get_by_id(db, vendor_id)
        if not vendor:
            raise NotFoundException("Vendor", str(vendor_id))
        vendor = vendor_repository.update(db, vendor, payload)
        return VendorResponse.model_validate(vendor)

    def delete_vendor(self, db: Session, vendor_id: int) -> None:
        vendor = vendor_repository.get_by_id(db, vendor_id)
        if not vendor:
            raise NotFoundException("Vendor", str(vendor_id))
        vendor_repository.delete(db, vendor)


vendor_service = VendorService()
