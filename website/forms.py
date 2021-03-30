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


class OrderChoiceField(ChoiceField):
    def __init__(self,**kwargs):
        self.choices = [('Descendente','DESC'),('Ascendente','ASC'),]
        super().__init__(choices=self.choices,**kwargs)


class ObjectiveForm(ModelForm):
    class Meta:
        model = Objective
        fields = ['metric','description']
    order = OrderChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs = {'class' : "form-control"}
        # self.fields['order'].widget=widgets.ChoiceWidget(attrs={'class': 'form-control'})
