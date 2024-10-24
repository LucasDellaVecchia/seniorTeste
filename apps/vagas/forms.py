from django import forms
from apps.vagas.models import Vagas, Candidatos
from datetime import datetime

ESCOLARIDADE = (
    ('Ensino Fundamental', 'Ensino Fundamental'),
    ('Ensino Médio', 'Ensino Médio'),
    ('Tecnólogo', 'Tecnólogo'),
    ('Ensino Superior', 'Ensino Superior'),
    ('Pós / MBA / Mestrado', 'Pós / MBA / Mestrado'),
    ('Doutorado', 'Doutorado'),
)

FAIXA_SALARIAL = (
    ('Até 1.000', 'Até 1.000'),
    ('De 1.000 a 2.000', 'De 1.000 a 2.000'),
    ('De 2.000 a 3.000', 'De 2.000 a 3.000'),
    ('Acima de 3.000', 'Acima de 3.000')
)
    

class VagasForms(forms.ModelForm):

    nome = forms.CharField(
        label="Vaga",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nome da Vaga"
            }
        )
    )

    faixa = forms.ChoiceField(
        choices=FAIXA_SALARIAL
    )

    escolaridade = forms.ChoiceField(
        choices=ESCOLARIDADE
    )

    requisitos = forms.CharField(
        label="Requisitos",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Requisitos"
            }
        )
    )

    class Meta:
        model = Vagas
        exclude = ["empresa", "data"]


class CandidatosForms(forms.ModelForm):

    vaga = forms.ModelChoiceField(
        queryset=Vagas.objects.all().order_by("nome"),
        label="Vaga",
        empty_label="Selecione a Vaga",
        required=True,
        widget = forms.Select(
            attrs = {
                "class": "form-control"
            }
        )
    )

    pretensao = forms.CharField(
        label="Pretensão Salarial",
        required=True,
        max_length=50,
        widget= forms.TextInput(
            attrs = {
                "class": "form-control"
            }
        )
    )

    experiencia = forms.CharField(
        label="Experiência",
        required=True,
        widget= forms.TextInput(
            attrs = {
                "class": "form-control"
            }
        )
    )

    escolaridade = forms.ChoiceField(
        choices=ESCOLARIDADE,
        required=True
    )

    class Meta:
        model = Candidatos
        exclude = ["usuario", "data"]