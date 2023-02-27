from fastapi import FastAPI

from users.views import router_user
from plane.views import router_plane
from order.views import router_order
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "User",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Plane",
        "description": "Operations with plane. Create plane, seat and route is here.",
    },
    {
        "name": "Route",
        "description": "Operations with route. Create route and get routes by city names.",
    },
    {
        "name": "Order",
        "description": "Operations with order. Create order and calculate order with seat and route is here.",
    },
]
app = FastAPI(
    title='Masc Airlines api',
    description='Api of company Masc Airlines',
    redoc_url='/',
    contact={
        'name': 'mascDriver',
        'url': 'https://mascdriver.com.br',
        'email': 'diogobaltazardonascimento@outlook.com',
    },
    openapi_tags=tags_metadata
)
origins = [
    "http://localhost",
    "http://localhost:8001",
    "http://localhost:19006",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_user)
app.include_router(router_plane)
app.include_router(router_order)
