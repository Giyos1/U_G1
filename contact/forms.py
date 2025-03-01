from django import forms
from urllib3 import request

from contact.models import Contact


class ContactForms(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(error_messages={"invalid": "email xato"},
                             widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "email kiriting"}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    # password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    # re_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 3:
            raise forms.ValidationError("nameni 3 tadan kichik berish mumkin emas")
        return name

    # def clean(self):
    #     password = self.cleaned_data.get("password")
    #     re_password = self.cleaned_data.get("re_password")
    #
    #     if password != re_password:
    #         raise forms.ValidationError("ikkta xar xil password")
    #     return self.cleaned_data

    def save(self):
        return Contact.objects.create(**self.cleaned_data)

    def update(self, instance):
        instance.name = self.clean_name()
        instance.phone = self.cleaned_data.get("phone")
        instance.address = self.cleaned_data.get("address")
        instance.email = self.cleaned_data.get("email")
        instance.save()
        return instance


class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "address"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'emailingizni kiriting!'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'email': {'invalid': 'Email is invalid ekanku aka'},
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError('Name must be at least 3 characters long')
        return name

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        if not phone.startswith('+998'):
            self.add_error('phone', 'Phone number must start with +998')
        return cleaned_data

    def save(self, commit=True):
        # if self.instance:
        #     return Contact.objects.filter(id=self.instance.id).update(**self.cleaned_data)
        return Contact.objects.create(created_by=self.files.get("request").user, **self.cleaned_data)
