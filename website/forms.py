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
            self.add_error('email','The email provided is not registered with us, '
                                   'please try to contact administration.')



