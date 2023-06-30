from django import forms

class LoginForms(forms.Form):
    login=forms.CharField(
        label='Login', 
        required=True, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Mario Silva',
            }
        )
    )
    password=forms.CharField(
        label='Password', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha',
            }
        ),
    )

