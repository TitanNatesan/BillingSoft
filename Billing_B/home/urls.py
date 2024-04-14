from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.home, name='Home'),
    path('makereceipt/', views.makeReciept, name='Make Loan'),
    path('customers/',views.dispCustomers,name='View Receipts'),
    path('user/<int:user_id>/details', views.user_details_individual, name='user_details_individual'),
    path('property/<int:pid>/details', views.property_details_individual, name='property_details_individual'),
    path('loan/<int:lid>/details', views.loan_details_individual, name='loan_details_individual'),
    path("update",views.updateDues,name="Update_Dues"), 
    # path('vr/<int:cid>/<int:pid>/',views.viewrec),    
    # path("view_records/",views.user_details,name='User Records'),
    # path('loan-details/<int:rid>/',views.loan_deat,name='Loan Details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
