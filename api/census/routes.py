from starlette.routing import Route

from census import views


routes = [
    Route('/find', views.find)
]
