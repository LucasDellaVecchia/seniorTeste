
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.vagas.models import Vagas, Candidatos
from apps.usuarios.forms import CadastroForms
from django.db.models import Count
from django.db.models.functions import TruncMonth

class CadastroUsuarioTests(TestCase):

    def test_cadastro_form_valid(self):
        form_data = {'login': 'test@example.com', 'senha': 'password123', 'tipo': 'Candidato'}
        form = CadastroForms(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cadastro_form_invalid(self):
        form_data = {'login': 'test@example.com', 'senha': '', 'tipo': 'Candidato'}
        form = CadastroForms(data=form_data)
        self.assertFalse(form.is_valid())

class VagasTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_create_vaga(self):
        vaga = Vagas.objects.create(
            nome="Desenvolvedor",
            faixa="3000-5000",
            escolaridade="Ensino Superior",
            requisitos="Python, Django",
            empresa=self.user
        )
        self.assertEqual(vaga.nome, "Desenvolvedor")
        self.assertEqual(vaga.empresa, self.user)

class CandidatosTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.vaga = Vagas.objects.create(
            nome="Desenvolvedor",
            faixa="3000-5000",
            escolaridade="Ensino Superior",
            requisitos="Python, Django",
            empresa=self.user
        )

    def test_create_candidato(self):
        candidato = Candidatos.objects.create(
            usuario=self.user,
            vaga=self.vaga,
            pretensao="4000",
            experiencia="3 anos em Python",
            escolaridade="Ensino Superior"
        )
        self.assertEqual(candidato.usuario, self.user)
        self.assertEqual(candidato.vaga, self.vaga)
        self.assertEqual(candidato.pretensao, "4000")

class IndexViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/login/')

    def test_logged_in_user_sees_vagas(self):
        self.client.login(username='testuser', password='password123')
        Vagas.objects.create(nome='Desenvolvedor', empresa=self.user)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Desenvolvedor')

    def test_vagas_count_annotation(self):
        self.client.login(username='testuser', password='password123')
        Vagas.objects.create(nome='Desenvolvedor', empresa=self.user)
        Vagas.objects.create(nome='Analista', empresa=self.user)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        vagas = response.context['form']
        for vaga in vagas:
            self.assertIsNotNone(vaga.candidatos)

class CadastroVagasViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_get_cadastro_form_when_logged_in(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cadastroVagas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros/cadastroVagas.html')

    def test_post_create_vaga(self):
        self.client.login(username='testuser', password='password123')
        form_data = {
            'nome': 'Engenheiro de Software',
            'faixa': '3000-5000',
            'escolaridade': 'Ensino Superior',
            'requisitos': 'Experiência com Python',
            'data': '2024-01-01'
        }
        response = self.client.post(reverse('cadastroVagas'), data=form_data)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(Vagas.objects.filter(nome='Engenheiro de Software').exists())

class GraficoVagasViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        Vagas.objects.create(nome='Desenvolvedor', empresa=self.user, data='2024-01-01')
        Vagas.objects.create(nome='Analista', empresa=self.user, data='2024-01-15')

    def test_logged_in_user_sees_graph_data(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('graficoVagas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'graficos/graficoVagas.html')

        # Verifica se os dados para o gráfico foram passados corretamente
        self.assertIn('meses', response.context)
        self.assertIn('total_vagas', response.context)
        self.assertEqual(len(response.context['meses']), 1)  # Apenas um mês, Janeiro 2024

