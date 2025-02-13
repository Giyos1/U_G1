from tkinter.font import names

from django.http import HttpResponse
from django.shortcuts import render, redirect

from contact.forms import ContactForms, ContactModelForm
from contact.models import Contact


def contact_list(request):
    all_contacts = Contact.objects.all()
    data = {
        "contacts": all_contacts,
    }
    return render(request, "contact/list.html", context=data)


def contact_create_form(request):
    forms = ContactModelForm()
    return render(request, "contact/create.html", {"forms": forms})


def contact_create(request):
    forms = ContactModelForm(request.POST)
    if forms.is_valid():
        forms.save()
        return redirect("contacts:contact_list")
    # name = request.POST.get("name")
    # email = request.POST.get("email")
    # phone = request.POST.get("phone")
    # address = request.POST.get("address")
    # Contact.objects.create(name=name, email=email, phone=phone, address=address)
    return render(request, "contact/create.html", {"forms": forms})


def contact_edit(request, pk):
    if request.method == "POST":
        contact = Contact.objects.get(id=pk)
        forms = ContactModelForm(request.POST, instance=contact)
        if forms.is_valid():
            forms.save()
            # name = request.POST.get("name")
            # email = request.POST.get("email")
            # phone = request.POST.get("phone")
            # address = request.POST.get("address")
            # Contact.objects.filter(pk=pk).update(name=name, email=email, phone=phone, address=address)
            return redirect("contacts:contact_list")
        return render(request, "contact/edit.html", {"forms": forms, "contact": contact})
    contact = Contact.objects.get(pk=pk)
    forms = ContactModelForm(instance=contact)
    return render(request, "contact/edit.html", context={"contact": contact, "forms": forms})


def contact_delete(request, pk):
    Contact.objects.filter(pk=pk).delete()
    return redirect("contacts:contact_list")


def contact_detail(request, pk):
    contact = Contact.objects.get(pk=pk)
    return render(request, "contact/detail.html", context={"contact": contact})
