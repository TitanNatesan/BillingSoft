from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.home, name='Home'),
    path('makereceiptNC/', views.makeRecieptNC, name='Make Receipt'),
    path('vr/<int:cid>/<int:pid>/',views.viewrec),    
    path('view_receipts/',views.dispReceipts,name='View Receipts'),
    path("view_records/",views.user_details,name='User Records'),
    path('user/<int:user_id>/details', views.user_details_individual, name='user_details_individual'),
    path('loan-details/<int:rid>/',views.loan_deat,name='Loan Details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
