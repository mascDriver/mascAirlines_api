from fastapi import FastAPI

from users.views import router_user
from plane.views import router_plane
from order.views import router_order

app = FastAPI(
    title='Masc Airlines api',
    description='Api of company Masc Airlines',
    redoc_url='/',
    contact={
        'email': 'diogobaltazardonascimento@outlook.com',
    }
)


app.include_router(router_user)
app.include_router(router_plane)
app.include_router(router_order)
