from fastapi import FastAPI

from users.views import router_user
from plane.views import router_plane
from order.views import router_order

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


app.include_router(router_user)
app.include_router(router_plane)
app.include_router(router_order)
