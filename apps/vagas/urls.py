from django.urls import path, include
from apps.vagas.views import index, cadastroVagas, editarVagas, deletarVagas, indexCandidato, candidatarVaga, graficoVagas, graficoCandidatos, graficoCandidatosVaga, \
VagasViewSet, CandidatosViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register("vagas", VagasViewSet, basename="Vagas")
router.register("candidatos", CandidatosViewSet, basename="Candidatos")

urlpatterns = [
    path("index", index, name="index"),
    path("indexCandidato", indexCandidato, name="indexCandidato"),
    path("candidatarVaga", candidatarVaga, name="candidatarVaga"),
    path("cadastroVagas", cadastroVagas, name="cadastroVagas"),
    path("editarVagas/<int:pk>/", editarVagas, name="editarVagas"),
    path("deletarVagas/<int:pk>/", deletarVagas, name="deletarVagas"),
    path("graficoVagas", graficoVagas, name="graficoVagas"),
    path("graficoCandidatos", graficoCandidatos, name="graficoCandidatos"),
    path("graficoCandidatos/<int:pk>/", graficoCandidatosVaga, name="graficoCandidatosVaga"),
    path("", include(router.urls))
]