from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

ESCOLARIDADE = (
    ('Ensino Fundamental', 'Ensino Fundamental'),
    ('Ensino Médio', 'Ensino Médio'),
    ('Tecnólogo', 'Tecnólogo'),
    ('Ensino Superior', 'Ensino Superior'),
    ('Pós / MBA / Mestrado', 'Pós / MBA / Mestrado'),
    ('Doutorado', 'Doutorado')
)

class Vagas(models.Model):

    nome = models.CharField(
        max_length=150,
        null=False,
        blank=False
    )

    faixa = models.CharField(
        max_length=30,
        null=False,
        blank=False
    )

    escolaridade = models.CharField(
        max_length=25,
        null=False,
        blank=False
    )

    requisitos = models.TextField(
        null=False,
        blank=False
    )

    empresa = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    data = models.DateField(
        null=False,
        blank=False
    )

    def __str__(self):
        return self.nome
    


class Candidatos(models.Model):

    usuario = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        
    )

    vaga = models.ForeignKey(
        Vagas,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="vagas",
        verbose_name="Vaga"
    )

    pretensao = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        default=""
    )

    experiencia = models.TextField(
        null=False,
        blank=False,
        default=""
    )

    escolaridade = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        choices=ESCOLARIDADE
    )

    data = models.DateField(
        null=False,
        blank=False
    )
