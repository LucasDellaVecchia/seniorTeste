from django.test import TestCase
from django.urls import reverse
from apps.usuarios.forms import LoginForms

class LoginTests(TestCase):

    def test_login_form_valid(self):
        form_data = {'login': 'test@example.com', 'senha': 'password123'}
        form = LoginForms(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form_data = {'login': '', 'senha': 'password123'}
        form = LoginForms(data=form_data)
        self.assertFalse(form.is_valid())
