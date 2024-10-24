from django.shortcuts import render, redirect
from apps.usuarios.forms import LoginForms, CadastroForms
from django.contrib import auth
from django.contrib.auth.models import User


def login(request):
    form = LoginForms()
    botao = request.GET.get("botao")
    if botao == "cadastrar":
        return redirect("cadastroUsuarios")

    if request.method == "POST":
        form = LoginForms(request.POST)

        if form.is_valid():
            nome = form["login"].value()
            senha = form["senha"].value()

            usuario = auth.authenticate(request, username=nome, password=senha)

            if usuario is None:
                return redirect("login")
            else:
                auth.login(request, usuario)
                if usuario.is_superuser:
                    return redirect("index")
                else:
                    return redirect("indexCandidato")
  
    return render(request, "login.html", {"form": form})


def cadastroUsuarios(request):
    form = CadastroForms()

    if request.method == "POST":
        form = CadastroForms(request.POST)

        if form.is_valid():
            usuario = form["login"].value()
            senha = form["senha"].value()
            tipo = form["tipo"].value()

            if User.objects.filter(username=usuario).exists():
                return redirect("login")
            
            if tipo == "Empresa":
                usuario = User.objects.create_superuser(
                    username=usuario,
                    password=senha
                )
                usuario.save()

                auth.login(request, usuario)
                return redirect("index")
            
            else:
                usuario = User.objects.create_user(
                    username=usuario,
                    password=senha
                )
                usuario.save()

                auth.login(request, usuario)
                return redirect("indexCandidato")

            
        else:
            print(form.errors)
        
    return render(request, "cadastros/cadastro.html", {"form": form})
        

def logout(request):
    auth.logout(request)
    return redirect("login")
