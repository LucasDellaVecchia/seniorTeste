from django import forms

OPCOES = [
        ('Empresa', 'Empresa'),
        ('Candidato', 'Candidato'),
    ]

class LoginForms(forms.Form):

    login = forms.CharField(
        label="Usuário",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Usuário"
            }
        )
    )

    senha = forms.CharField(
        label="Senha",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite sua senha"
            }
        )
    )


class CadastroForms(forms.Form):

    login = forms.CharField(
        label="Usuário",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Usuário"
            }
        )
    )

    senha = forms.CharField(
        label="Senha",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite sua senha"
            }
        )
    )

    tipo = forms.ChoiceField(
        label="Selecione o tipo",
        choices=OPCOES,
        widget=forms.RadioSelect,
        required=True
    )