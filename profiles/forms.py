"""from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

from profiles.models import CustomUser, AddWalletAddress, Kyc


User = get_user_model()


class UserLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']= 'form-control p_input'
        self.fields['password'].widget.attrs['class']= 'form-control p_input'



class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['id']= 'password1'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control p_input"
        
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfilesForm(forms.ModelForm):
    profile_picture = forms.ImageField(label=('Profile Picture'),required=False, widget=forms.FileInput)
    remove_photo = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(ProfilesForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['id'] = field
        # self.fields['profile_picture'].widget.attrs['onchange']=  "submit();"


    class Meta:
        model = CustomUser
        fields = ["profile_picture", "first_name", "last_name", "gender", "date_of_birth", "address1", "state", "city", "country"]
        required = ["first_name", "last_name", "gender", "date_of_birth", "address1", "state", "city", "country"]


class MyPasswordChangeForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


# class MyPasswordChangeForm(forms.Form):
#     old_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'autocomplete': 'password', 'class': 'form-control'}),
#     )
#     new_password1 = forms.CharField(
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
#     )
#     new_password2 = forms.CharField(
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
#     )


class AddWalletAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddWalletAddressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'
        
    class Meta:
        model = AddWalletAddress
        exclude= ['user']


class KycForm(forms.ModelForm):
    def __init__(self, *args,  **kwargs):
        super(KycForm, self).__init__(*args, **kwargs)
        self.fields['card_type'].widget.attrs['class'] = 'form-control'
        self.fields['face_with_id'].widget.attrs['class'] = 'form-control upload_inp mt-2'
        self.fields['card_front'].widget.attrs['class'] = 'form-control upload_inp mt-2'
        self.fields['card_back'].widget.attrs['class'] = 'form-control upload_inp mt-2'
        self.fields['address_proof'].widget.attrs['class'] = 'form-control'


    class Meta:
        model = Kyc
        exclude = ['user']
"""