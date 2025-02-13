from django import forms

from contact.models import Contact


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'emailingizni kiriting!'}),
        error_messages={'invalid': 'Email is invalid ekanku aka'})
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

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
        return Contact.objects.create(**self.cleaned_data)

    def update(self, instance):
        instance.name = self.cleaned_data.get('name')
        instance.email = self.cleaned_data.get('email')
        instance.phone = self.cleaned_data.get('phone')
        instance.address = self.cleaned_data.get('address')
        instance.save()
        return instance



class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'address']
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

    def update(self, instance):
        """ ModelForm da `update` uchun qo'shimcha method """
        for field in self.cleaned_data:
            setattr(instance, field, self.cleaned_data[field])
        instance.save()
        return instance

