from django.urls import path
from apps.usuarios.views import login, cadastroUsuarios, logout


urlpatterns = [
    path("login/", login, name="login"),
    path("cadastroUsuarios/", cadastroUsuarios, name="cadastroUsuarios"),
    path("logout/", logout, name="logout"),
]