from django.http import HttpResponse
from django.shortcuts import render, redirect

from contact.forms import ContactForm, ContactModelForm
from contact.models import Contact


def contact_list(request):
    all_contacts = Contact.objects.all()
    data = {
        "contacts": all_contacts,
    }
    return render(request, "contact/list.html", context=data)


def contact_create_form(request):
    forms = ContactModelForm()
    return render(request, "contact/create.html", context={"forms": forms})


def contact_create(request):
    forms = ContactModelForm(request.POST)
    if not forms.is_valid():
        return render(request, "contact/create.html", context={"forms": forms})
    forms.save()
    return redirect("contacts:contact_list")


def contact_edit(request, pk):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.update(Contact.objects.get(pk=pk))
            return redirect("contacts:contact_list")
        return render(request, "contact/edit.html", context={"forms": form, "contact": Contact.objects.get(pk=pk)})
    contact = Contact.objects.get(pk=pk)
    forms = ContactForm(
        initial={
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "address": contact.address,
        }
    )
    return render(request, "contact/edit.html", context={"contact": contact, "forms": forms})


def contact_delete(request, pk):
    Contact.objects.filter(pk=pk).delete()
    return redirect("contacts:contact_list")


def contact_detail(request, pk):
    contact = Contact.objects.get(pk=pk)
    return render(request, "contact/detail.html", context={"contact": contact})
