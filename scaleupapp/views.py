from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .forms import NewUserForm, CompanyDetailsForm, CompanyDetailsRemarksPivoteForm
from django.contrib.auth.models import Group, User
from .models import CompanyDetails, CompanyDetailsRemarkPivot,CatalogueStatus

from django.core.paginator import Paginator
import pandas as pd
objects_per_page = 25
# Create your views here.
@login_required
def home(request):
    return render(request, 'scaleupapp/index.html')

class UserRegister(TemplateView):
    def get(self, request):
        forms = NewUserForm()
        return render(request, "scaleupapp/auth/register.html", context={'forms': forms})
    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # group = Group.objects.filter(name='user')
            # user.groups.add(group)
            # user.groups.set([group])

            messages.success(request, "Registration successful.")
            login(request, user)
            messages.success(
                request, f"You are now logged in as {user.username}.")
            return redirect("home")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
        forms = NewUserForm()
        return render(request, "scaleupapp/auth/register.html", context={'forms': forms})


class LoginwithEmail(TemplateView):
    
    def get(self, request):
        return render(request, "scaleupapp/auth/login.html")
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        User = get_user_model()
        checkuseremail = User.objects.filter(email=email).first()
        if checkuseremail :
            user = authenticate(request, username=checkuseremail.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('login')
        else :
            messages.error(request, 'Invalid email or password.')
            return redirect('login')


def userlogout(request):
    logout(request)
    return redirect(reverse('login'))

class CompanyDetailsExport(TemplateView):
    def get(self, request):
        catalogueStatus = CatalogueStatus.objects.all()
        user = User.objects.all()
        return render(request, "scaleupapp/compnydetails/exportcompanydetails.html", context={'user':user,'catalogueStatus':catalogueStatus})
    def post(self, request):
        catalogue_status = request.POST.get('catalogue_status')
        user_name = request.POST.get('user_name')
        filtered_data = CompanyDetails.objects.filter(user=user_name, catalogue_status=catalogue_status).all()
        filtered_data = filtered_data.values()
        for item in filtered_data:
            item['created_at'] = item['created_at'].astimezone(timezone.utc).replace(tzinfo=None)
            item['updated_at'] = item['updated_at'].astimezone(timezone.utc).replace(tzinfo=None)
        df = pd.DataFrame(list(filtered_data))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
        df.to_excel(response, index=False, sheet_name='Sheet1')

        return response

class CompanyDetailsImport(TemplateView):
    def get(self, request):
        user = User.objects.all()
        return render(request, "scaleupapp/compnydetails/importcompanydetails.html", context={'user':user})
    def post(self, request):
        excel_file = request.FILES['excel_file']
        userName = request.POST.get('user_name')
        if(userName):
            user_id = User.objects.filter(id=userName).first()
            df = pd.read_excel(excel_file, header=None)
            for index, row in df.iterrows():
                obj = CompanyDetails.objects.filter(mobile=row[1]).first()
                if obj:
                    obj.business_name = row[1]
                else:
                    obj = CompanyDetails()
                    obj.business_name = row[1]
                    obj.mobile = row[0]
                    obj.user = user_id
                obj.save()
            messages.success(request, "Compnay Details Added successful.")
            return redirect("list-compnay-details")
        else:
            messages.error(request, "Please Select User Name")

class CompanyDetailsCreate(TemplateView):
    def get(self, request):
        forms = CompanyDetailsForm()
        return render(request, "scaleupapp/compnydetails/addcompanydetails.html", context={'forms':forms})
    def post(self, request):
        form = CompanyDetailsForm(request.POST)
        if form.is_valid():
            companydetails = form.save()
            companydetails.user = request.user
            companydetails.save()
            messages.success(request, "Compnay Details Added successful.")
            return redirect("list-compnay-details")
        messages.error(
            request, "Compnay Details Not Added")
        forms = CompanyDetailsForm()
        return render(request, "scaleupapp/compnydetails/addcompanydetails.html", context={'forms':forms})
    

class CompanyDetailsList(TemplateView):
    def get(self, request):
        catalogueStatus = CatalogueStatus.objects.all()
        user = User.objects.all()
        companyDetails = CompanyDetails.objects.filter(user=request.user).all()
        catalogue_status = request.GET.get('catalogue_status')
        user_name = request.GET.get('user_name')
        if user_name:
            companyDetails = companyDetails.filter(user=user_name)
        if catalogue_status:
            # catalogue_Status_data = CatalogueStatus.objects.filter(id=catalogue_status).first()
            companyDetails = companyDetails.filter(catalogue_status=catalogue_status)
        paginator = Paginator(companyDetails, objects_per_page)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)
        return render(request, "scaleupapp/compnydetails/listcompanydetails.html", context={'user': user, 'catalogueStatus': catalogueStatus,'page_objects':page_objects})
def viewCompanyDetails(request, id):
    companyDetails = CompanyDetails.objects.filter(user=request.user, pk=id).first()
    changelog = CompanyDetailsRemarkPivot.objects.filter(company_details=companyDetails).order_by('-id').all()
    return render(request, "scaleupapp/compnydetails/viewcompanydetails.html", context={'companyDetails':companyDetails, 'changelog':changelog})
class CompanyDetailsUpdate(TemplateView):
    def get(self, request, id):
        
        return render(request, "scaleupapp/compnydetails/listcompanydetails.html")
    
def CompanyDetailsChange(request, id):
        companyDetails = CompanyDetails.objects.filter(user=request.user, pk=id).first()
        if request.method == 'POST':
            forms = CompanyDetailsRemarksPivoteForm(request.POST)
            if forms.is_valid():
                companydetailsremarks = forms.save()
                companydetailsremarks.user = request.user
                companydetailsremarks.company_details = companyDetails
                companydetailsremarks.save()

                companyDetails.catalogue_status = companydetailsremarks.catalogue_status
                companyDetails.save()
                messages.success(request, "Remarks Added successfully!!")
                return redirect("list-compnay-details")
        forms = CompanyDetailsRemarksPivoteForm()
        changelog = CompanyDetailsRemarkPivot.objects.filter(company_details=companyDetails).order_by('-id').all()

        return render(request, "scaleupapp/compnydetails/changecompanydetails.html", context={'forms':forms, 'companyDetails':companyDetails, 'changelog':changelog})


def CompanyDetailsEdit(request, id):
    companyDetails = CompanyDetails.objects.filter(user=request.user, pk=id).first()
    if request.method == 'POST':
        forms = CompanyDetailsForm(request.POST, instance=companyDetails)
        if forms.is_valid():
            companydetails = forms.save()
            companydetails.user = request.user
            companydetails.save()
            messages.success(request, "Details Updated successfully!!")
            return redirect("list-compnay-details")
    forms = CompanyDetailsForm(instance=companyDetails)
    return render(request, "scaleupapp/compnydetails/updatecompanydetails.html", context={'forms':forms, 'companyDetails':companyDetails})
