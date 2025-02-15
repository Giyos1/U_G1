from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from contact.forms import ContactModelForm
from contact.models import Contact


def contact_list(request):
    q = request.GET.get("q")
    all_contacts = Contact.objects.all()
    if q:
        all_contacts = all_contacts.filter(Q(name__icontains=q) | Q(phone__icontains=q))

    # pagination
    paginator = Paginator(all_contacts, 5)
    page_number = request.GET.get("page")
    all_contacts = paginator.get_page(page_number)
    data = {
        "q": q,
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
