from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine
from plane import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

router_plane = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_plane.post("/plane/", response_model=schemas.Plane)
async def create_plane(plane: schemas.Plane, db: Session = Depends(get_db)):
    return crud.create_db_plane(db=db, plane=plane)


@router_plane.get("/plane/{plane_id}", response_model=schemas.Plane)
async def read_plane(plane_id: int, db: Session = Depends(get_db)):
    db_plane = crud.get_plane(db, plane_id=plane_id)
    if db_plane is None:
        raise HTTPException(status_code=404, detail="Plane not found")
    return db_plane


@router_plane.post("/seat/", response_model=schemas.Seat)
async def create_seat(seat: schemas.SeatCreate, db: Session = Depends(get_db)):
    return crud.create_db_seat(db=db, seat=seat)


@router_plane.get("/seat/{seat_id}", response_model=schemas.Seat)
async def read_seat(seat_id: int, db: Session = Depends(get_db)):
    db_seat = crud.get_seat(db, seat_id=seat_id)
    if db_seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    return db_seat


@router_plane.post("/route/", response_model=schemas.Route)
async def create_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    return crud.create_db_route(db=db, route=route)


@router_plane.get("/route/{route_id}", response_model=schemas.Route)
async def read_seat(route_id: int, db: Session = Depends(get_db)):
    db_route = crud.get_route(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route
