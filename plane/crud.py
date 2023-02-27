from sqlalchemy.orm import Session
from sqlalchemy import func

from plane import models, schemas


def create_db_plane(db: Session, plane: schemas.Plane):
    db_plane = models.Plane(**plane.dict())
    db.add(db_plane)
    db.commit()
    db.refresh(db_plane)
    return db_plane


def get_plane(db: Session, plane_id: int):
    return db.query(models.Plane).filter(models.Plane.id == plane_id).first()


def get_num_seat_by_plane(db: Session, plane_id: int):
    return db.query(models.Seat.id).filter(models.Seat.plane_id == plane_id).count()


def create_db_seat(db: Session, seat: schemas.SeatCreate):
    sum_seats = get_num_seat_by_plane(db, seat.plane_id)
    seat_dict = seat.dict()
    db_seat = models.Seat(**seat_dict, number=sum_seats+1)
    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)
    return db_seat


def get_seat(db: Session, seat_id: int):
    return db.query(models.Seat).filter(models.Seat.id == seat_id).first()


def create_db_route(db: Session, route: schemas.RouteCreate):
    route_dict = route.dict()
    db_route = models.Route(**route_dict)
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


def get_route(db: Session, route_id: int):
    return db.query(models.Route).filter(models.Route.id == route_id).first()


def get_route_by_city(db: Session, origin_id: int, destiny_id: int):
    return db.query(models.Route).filter(models.Route.origin_id == origin_id, models.Route.destiny_id == destiny_id).all()


def get_seat_by_number(db: Session, number: int, plane_id: int):
    return db.query(models.Seat).filter(models.Seat.number == number, models.Seat.plane_id == plane_id).first()
