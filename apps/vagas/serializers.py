from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from apps.vagas.models import Vagas, Candidatos


class VagasSerializer(serializers.ModelSerializer):
    candidatos = serializers.IntegerField(read_only=True)

    class Meta:
        model = Vagas
        fields = ["id", "nome", "faixa", "requisitos", "escolaridade", 'candidatos']

    def create(self, validated_data):

        usuario = self.context["request"].user
        if not usuario.is_superuser:
            raise PermissionDenied("Você não tem permissão para criar vagas!")
        
        return Vagas.objects.create(empresa=usuario, **validated_data)
    

class CandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidatos
        fields = ["usuario", "vaga", "pretensao", "experiencia", "escolaridade"]
