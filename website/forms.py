from django.forms import *
from .models import *


class LoginForm(Form):
    email = fields.EmailField()
    password = fields.CharField()

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = widgets.TextInput(attrs={'class': 'page-login-field top-15  form-control',
                                                                  'placeholder': 'Email Address'})
        self.fields['email'].required = False
        self.fields['email'].validators = [self.validate_user_exist]
        self.fields['password'].required = False
        self.fields['password'].widget = widgets.PasswordInput(
            attrs={'class': 'page-login-field bottom-20 form-control','placeholder': 'Password'})


    def validate_user_exist(self, field):
        """
        verifies if the user actually exists
        :param field: str: email provided
        :return: error if any
        """
        users = User.objects.filter(email=field)
        if not users:
            self.add_error('email','El correo proveido no esta registrado para acceder a esta plataforma.'
                                   'Favor de contactar al administador para resolver el problema.')


class ObjectiveForm(Form):
    metrica = CharField(max_length=30)
    descripcion = CharField(max_length=150, widget=Textarea())
    valor_de_acceptacion = CharField(max_length=100)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs = {'class' : "form-control"}
