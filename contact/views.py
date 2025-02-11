from django.http import HttpResponse
from django.shortcuts import render, redirect
from contact.models import Contact


def contact_list(request):
    all_contacts = Contact.objects.all()
    data = {
        "contacts": all_contacts,
    }
    return render(request, "contact/list.html", context=data)


def contact_create_form(request):
    return render(request, "contact/create.html")


def contact_create(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    Contact.objects.create(name=name, email=email, phone=phone, address=address)
    return redirect("contacts:contact_list")


def contact_edit(request, pk):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        Contact.objects.filter(pk=pk).update(name=name, email=email, phone=phone, address=address)
        return redirect("contacts:contact_list")
    contact = Contact.objects.get(pk=pk)
    return render(request, "contact/edit.html", context={"contact": contact})


def contact_delete(request, pk):
    Contact.objects.filter(pk=pk).delete()
    return redirect("contacts:contact_list")


def contact_detail(request, pk):
    contact = Contact.objects.get(pk=pk)
    return render(request, "contact/detail.html", context={"contact": contact})
