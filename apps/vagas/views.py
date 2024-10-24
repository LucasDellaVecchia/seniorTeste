from django.shortcuts import render, redirect
from apps.vagas.forms import VagasForms, CandidatosForms
from apps.vagas.models import Vagas, Candidatos
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.vagas.serializers import VagasSerializer, CandidatoSerializer
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

FAIXA_SALARIAL = {
    "Até 1.000": 1000,
    "De 1.000 a 2.000": 2000,
    "De 2.000 a 3.000": 3000,
    "Acima de 3.000": 4000
}

ESCOLARIDADE = {
     "Ensino Fundamental": 1,
     "Ensino Médio": 2,
     "Tecnólogo": 3,
     "Ensino Superior": 4,
     "Pós / MBA / Mestrado": 5,
     "Doutorado": 6
}


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_superuser:
        return redirect("indexCandidato")
    form = Vagas.objects.filter(empresa=request.user).annotate(candidatos=Count("vagas"))
    return render(request, "index.html", {"form":form})


def indexCandidato(request):
    if not request.user.is_authenticated:
        return redirect("login")
    form = Vagas.objects.all()
    
    return render(request, "indexCandidato.html", {"form":form})

def cadastroVagas(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_superuser:
        return redirect("indexCandidato")
    
    form = VagasForms()

    if request.method == "POST":
        form = VagasForms(request.POST)

        if form.is_valid():
            nome = form["nome"].value()
            faixa = form["faixa"].value()
            escolaridade = form["escolaridade"].value()
            requisitos = form["requisitos"].value()
            data = datetime.now().date()
            empresa = request.user

            if not Vagas.objects.filter(nome=nome, faixa=faixa, escolaridade=escolaridade, requisitos=requisitos, empresa=empresa, data=data).exists():
                vaga = Vagas.objects.create(
                    nome=nome,
                    faixa=faixa,
                    escolaridade=escolaridade,
                    requisitos=requisitos,
                    empresa=empresa,
                    data=data
                )
                vaga.save()

        return redirect("index")

    return render(request, "cadastros/cadastroVagas.html", {"form": form})


def editarVagas(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_superuser:
        return redirect("indexCandidato")
    
    registro = Vagas.objects.get(id=pk)
    form = VagasForms(instance=registro)
    candidatos = Candidatos.objects.filter(vaga=registro)
    for candidato in candidatos:
        auxiliar = 0
        try:
            if int(candidato.pretensao) <= FAIXA_SALARIAL[registro.faixa]:
                 auxiliar += 1
            if ESCOLARIDADE[candidato.escolaridade] >= ESCOLARIDADE[registro.escolaridade]:
                 auxiliar += 1
        except ValueError as e:
             pass
        
        candidato.avaliacao = auxiliar


    if request.method == "POST":
        form = VagasForms(request.POST, instance=registro)

        if form.is_valid():
            registro.nome = form["nome"].value()
            registro.faixa = form["faixa"].value()
            registro.escolaridade = form["escolaridade"].value()
            registro.requisitos = form["requisitos"].value()

            registro.save()
        return redirect("index")

    return render(request, "editarVagas.html", {"form": form, "pk": pk, "candidatos": candidatos})


def deletarVagas(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_superuser:
        return redirect("indexCandidato")

    registro = Vagas.objects.get(id=pk)
    if registro:
         registro.delete()
    
    return redirect("index")


def candidatarVaga(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    form = CandidatosForms()

    if request.method == "POST":
        form = CandidatosForms(request.POST)
        
        if form.is_valid():
            vaga = form["vaga"].value()
            pretensao = form["pretensao"].value()
            experiencia = form["experiencia"].value()
            escolaridade = form["escolaridade"].value()
            data = datetime.now().date()
            usuario = request.user

            vaga = Vagas.objects.get(id=vaga)

            if not Candidatos.objects.filter(vaga=vaga, pretensao=pretensao, experiencia=experiencia, escolaridade=escolaridade, usuario=usuario).exists():
                    candidato = Candidatos.objects.create(
                        vaga=vaga, 
                        pretensao=pretensao, 
                        experiencia=experiencia, 
                        escolaridade=escolaridade,
                        usuario=usuario,
                        data=data
                    )

                    candidato.save()

        return redirect("indexCandidato")
    
    return render(request, "cadastros/candidatarVaga.html", {"form": form})


"""GRÁFICOS"""
def graficoVagas(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_superuser:
        return redirect("indexCandidato")
    vagasMes = Vagas.objects.filter(empresa=request.user).annotate(
        mes=TruncMonth('data')
    ).values('mes').annotate(total_vagas=Count('id')).order_by('mes')

    meses = [v['mes'].strftime('%B %Y') for v in vagasMes]
    total_vagas = [v['total_vagas'] for v in vagasMes]

    # Passando os dados diretamente no contexto
    context = {
        'meses': meses,
        'total_vagas': total_vagas
    }

    return render(request, 'graficos/graficoVagas.html', context)


def graficoCandidatos(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_superuser:
        return redirect("indexCandidato")
    
    candidatosPorMmes = Candidatos.objects.filter(vaga__empresa=request.user).annotate(
        mes=TruncMonth('data')
    ).values('mes').annotate(totalCandidatos=Count('id')).order_by('mes')

    candidatos_por_vaga_mes = Candidatos.objects.filter(vaga__empresa=request.user).annotate(
        mes=TruncMonth('data')
    ).values('mes', 'vaga__nome').annotate(totalCandidatos=Count('id')).order_by('mes', 'vaga__nome')

    mesesCandidatos = [c['mes'].strftime('%Y-%m') for c in candidatosPorMmes]
    totalCandidatosGeral = [c['totalCandidatos'] for c in candidatosPorMmes]
    
    return render(request, "graficos/graficoCandidatos.html", {
        "meses_candidatos": mesesCandidatos,
        "total_candidatos_geral": totalCandidatosGeral,
    })


def graficoCandidatosVaga(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_superuser:
        return redirect("indexCandidato")

    try:
        vaga = Vagas.objects.get(id=pk)
    except Vagas.DoesNotExist:
        return render(request, 'erro.html', {'mensagem': 'Vaga não encontrada'})

    candidatosPorMes = Candidatos.objects.filter(vaga=vaga).annotate(
        mes=TruncMonth('data')
    ).values('mes').annotate(totalCandidatos=Count('id')).order_by('mes')

    labels = [entry['mes'].strftime('%Y-%m') for entry in candidatosPorMes]
    data = [entry['totalCandidatos'] for entry in candidatosPorMes]

    return render(request, 'graficos/graficoCandidatosVaga.html', {
        'vaga': vaga,
        'labels': labels,
        'data': data
    })


"""SERIALIZADORES"""
class VagasViewSet(viewsets.ModelViewSet):
     
    def get_queryset(self):
         usuario = self.request.user
         return Vagas.objects.filter(empresa=usuario).annotate(candidatos=Count("vagas"))
    serializer_class = VagasSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class CandidatosViewSet(viewsets.ModelViewSet):
    queryset = Candidatos.objects.all()
    serializer_class = CandidatoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    extra_kwargs = {
        'usuario': {'required': False},
        'data': {'required': False}
    }

    def create(self, request, *args, **kwargs):
        dados = request.data
        usuario = User.objects.filter(username=request.user).first()
        dados["usuario"] = usuario.pk
        dados["data"] = datetime.now().date()
        serializer = self.get_serializer(data=dados)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)