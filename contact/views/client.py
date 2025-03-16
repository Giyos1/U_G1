from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.http import HttpResponse
# from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import first

from accounts.utils import login_required
from contact.forms import ContactModelForm, UploadForm
from contact.models import Contact, UploadFile
from contact.utils import export_exel


@login_required()
def contact_list(request):
    q = request.GET.get("q")
    all_contacts = Contact.objects.filter(created_by=request.user)
    if q and q != "None":
        all_contacts = Contact.objects.search(q)

    # pagination
    paginator = Paginator(all_contacts, 5)
    page_number = request.GET.get("page")
    all_contacts = paginator.get_page(page_number)
    data = {
        "q": q,
        "contacts": all_contacts,
    }
    return render(request, "contact/list.html", context=data)


@login_required()
def contact_create_form(request):
    forms = ContactModelForm()
    return render(request, "contact/create.html", {"forms": forms})


@login_required()
def contact_create(request):
    forms = ContactModelForm(request.POST, instance=None)
    if forms.is_valid():
        forms.save(request=request)
        return redirect("contacts:contact_list")
    # name = request.POST.get("name")
    # email = request.POST.get("email")
    # phone = request.POST.get("phone")
    # address = request.POST.get("address")
    # Contact.objects.create(name=name, email=email, phone=phone, address=address)
    return render(request, "contact/create.html", {"forms": forms})


@login_required()
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


@permission_required('contact.delete_contact', raise_exception=True)
def contact_delete(request, pk):
    Contact.objects.filter(pk=pk).update(is_deleted=True)
    return redirect("contacts:contact_list")


@login_required()
def contact_detail(request, pk):
    contact = Contact.objects.get(pk=pk)
    return render(request, "contact/detail.html", context={"contact": contact})


def upload_file(request):
    if request.method == 'POST':
        # title = request.POST.get('title')
        # file = request.FILES.get('file')
        # if title and file:
        #     UploadFile.objects.create(title=title, file=file)
        #     return redirect('contacts:file_list')
        forms = UploadForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('contacts:file_list')
        return render(request, 'upload/upload_file.html', {'form': forms})
    forms = UploadForm()
    return render(request, 'upload/upload_file.html', {'form': forms})


def file_list(request):
    files = UploadFile.objects.all()
    return render(request, 'upload/file_list.html', {'files': files})


def update(request, pk):
    file = get_object_or_404(UploadFile, id=pk)
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES, instance=file)
        if form.is_valid():
            form.save()
            return redirect('contacts:file_list')
        return render(request, 'upload/update.html', {'form': form})
    form = UploadForm(instance=file)
    return render(request, 'upload/update.html', {'form': form})


def file_view(request, pk):
    file = get_object_or_404(UploadFile, id=pk)
    return render(request, 'upload/view.html', {'file': file})


@login_required()
def export(request):
    contact = Contact.objects.filter(created_by=request.user)
    path = request.build_absolute_uri(settings.MEDIA_URL, export_exel(contact.values()))
    # print(contact.values())
    return HttpResponse(path)
