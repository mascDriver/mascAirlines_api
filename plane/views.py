from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine
from plane import models, schemas, crud
from users import schemas as schemas_users, security as security_users, crud as crud_users

models.Base.metadata.create_all(bind=engine)

router_plane = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_plane.post("/plane/", response_model=schemas.Plane, tags=['Plane'])
async def create_plane(plane: schemas.Plane, db: Session = Depends(get_db),
                       seller: schemas_users.Seller = Depends(security_users.get_current_active_seller)):
    return crud.create_db_plane(db=db, plane=plane)


@router_plane.get("/plane/{plane_id}", response_model=schemas.Plane, tags=['Plane'])
async def read_plane(plane_id: int, db: Session = Depends(get_db)):
    db_plane = crud.get_plane(db, plane_id=plane_id)
    if db_plane is None:
        raise HTTPException(status_code=404, detail="Plane not found")
    return db_plane


@router_plane.post("/seat/", response_model=schemas.Seat, tags=['Plane'])
async def create_seat(seat: schemas.SeatCreate, db: Session = Depends(get_db),
                      seller: schemas_users.Seller = Depends(security_users.get_current_active_seller)):
    return crud.create_db_seat(db=db, seat=seat)


@router_plane.get("/seat/{seat_id}", response_model=schemas.Seat, tags=['Plane'])
async def read_seat(seat_id: int, db: Session = Depends(get_db)):
    db_seat = crud.get_seat(db, seat_id=seat_id)
    if db_seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    return db_seat


@router_plane.post("/route/", response_model=schemas.Route, tags=['Route'])
async def create_route(route: schemas.RouteCreate, db: Session = Depends(get_db),
                       seller: schemas_users.Seller = Depends(security_users.get_current_active_seller)):
    return crud.create_db_route(db=db, route=route)


@router_plane.get("/route/{route_id}", response_model=schemas.Route, tags=['Route'])
async def read_route(route_id: int, db: Session = Depends(get_db)):
    db_route = crud.get_route(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route


@router_plane.get("/city/", response_model=list[schemas_users.City], tags=['Route'])
async def get_city(city: str | None = Query(default='São Paulo', min_length=3, max_length=100), db: Session = Depends(get_db)):
    return crud_users.get_city(db, q=city)


@router_plane.get("/route/{origin_id}/{destiny_id}", response_model=list[schemas.Route], tags=['Route'])
async def read_route_by_city(origin_id: int, destiny_id: int, db: Session = Depends(get_db)):
    db_route = crud.get_route_by_city(db, origin_id=origin_id, destiny_id=destiny_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route


@router_plane.get("/seat/{plane_id}/", response_model=list[schemas.Seat], tags=['Plane'])
async def read_route_by_city(plane_id: int, type_seat: str = Query(), db: Session = Depends(get_db)):
    db_seat = crud.get_seat_by_plane(db, type_seat=type_seat, plane_id=plane_id)
    if db_seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    return db_seat
