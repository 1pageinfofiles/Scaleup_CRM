from django.urls import path, include
from . import views
from . import googlemap
urlpatterns = [
    path('', views.home, name="home"),
    path('google/map/search', googlemap.GoogleMapDataExtractor.as_view(), name="map-search-keywords"),
    path('login', views.LoginwithEmail.as_view(), name='login'),
    path('logout', views.userlogout, name='logout'),
    path('register', views.UserRegister.as_view(), name='register'),
    path('import/company/info', views.CompanyDetailsImport.as_view(), name="import-compnay-details"),
    path('export/company/info', views.CompanyDetailsExport.as_view(), name="export-compnay-details"),
    path('add/company/info', views.CompanyDetailsCreate.as_view(), name="add-compnay-details"),
    path('list/company/info', views.CompanyDetailsList.as_view(), name="list-compnay-details"),
    path('view/company/info/<int:id>', views.viewCompanyDetails, name="view-compnay-details"),
    path('change/company/info/<int:id>', views.CompanyDetailsChange, name="change-compnay-details"),
    path('edit/company/info/<int:id>', views.CompanyDetailsEdit, name="edit-compnay-details"),
]