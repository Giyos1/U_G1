from django.core.paginator import Paginator
# from django.db.models import Q
from django.shortcuts import render, redirect

from accounts.utils import login_required
from contact.forms import ContactModelForm
from contact.models import Contact, UploadedFile


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
    forms = ContactModelForm(request.POST, request.FILES)
    if forms.is_valid():
        # c = forms.save(commit=False)
        # c.created_by = request.user
        # c.save()
        forms.save()
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


@login_required()
def contact_delete(request, pk):
    Contact.objects.filter(pk=pk).update(is_deleted=True)
    return redirect("contacts:contact_list")


@login_required()
def contact_detail(request, pk):
    contact = Contact.objects.get(pk=pk)
    return render(request, "contact/detail.html", context={"contact": contact})


from contact.forms import UploadFileForm


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contacts:file_list')  # Fayllar ro‘yxatiga qaytarish
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

# def upload_file(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         file = request.FILES.get('file')
#
#         if title and file:  # Agar fayl va sarlavha mavjud bo'lsa
#             UploadedFile.objects.create(title=title, file=file)
#             return redirect('contacts:contact_list')  # Yuklangan fayllar sahifasiga yo‘naltirish
#     return render(request, 'upload.html')

def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'file_list.html', {'files': files})