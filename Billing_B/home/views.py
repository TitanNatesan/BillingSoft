# views.py
import random
from .models import Property, Customer, Reciept, Address
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.template import loader
from django.http import HttpResponse
from django.db import transaction
from django.template.loader import get_template


def home(request):
    return render(request, 'home.html', {})


@transaction.atomic
def makeRecieptNC(request):
    if request.method == "POST": 
        customer_type = request.POST.get('customer_type')
        
        property_name = request.POST.get('property_name')
        property_description = request.POST.get('property_description')
        property_value = request.POST.get('property_value')
        property_weight_gram = request.POST.get('property_weight_gram')
        property_weight_milligram = request.POST.get('property_weight_milligram')
        property_pic = request.FILES.get('property_pic')
        
        propert = Property(
            name=property_name,
            description=property_description,
            value=property_value,
            weight_grams=property_weight_gram,
            weight_milligrams=property_weight_milligram,
            pic=property_pic,
        )
        propert.save()
        
        if customer_type == 'existing':
            customer_id = request.POST.get('customer_id')
            customer = Customer.objects.get(pk=customer_id)
        
        if customer_type == 'new':
            # Retrieve customer details
            customer_name = request.POST.get('customer_name')
            customer_age = request.POST.get('customer_age')
            customer_phone = request.POST.get('customer_phone')
            customer_pic = request.FILES.get('customer_pic')
            address_line_1 = request.POST.get('addressline_1')
            address_line_2 = request.POST.get('addressline_2')
            city = request.POST.get('city')
            postal_code = request.POST.get('postal_code')
            state = request.POST.get('state')
            land_mark = request.POST.get('landmark')
            address = Address(
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                postal_code=postal_code,
                state=state,
                land_mark=land_mark,
                phone=customer_phone,
            )
            address.save()
            customer = Customer(
                name=customer_name,
                age=customer_age,
                pic=customer_pic,
                property=propert,
                address=address,
            )
            customer.save()

        loan_amount = request.POST.get('loan_amount')
        interest_rate = request.POST.get('interest_rate')
        total_dues = request.POST.get('total_dues')
        recipt = Reciept(
            customer=customer,
            property=propert,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            total_dues=total_dues,
        )
        recipt.save()
        template = get_template('reciept.html')
        cont ={
            'name':customer.name,
            'age':customer.age,
            'phone':customer.address.phone, 
            'property':propert.name,
            'date':recipt.when,
            'image':customer.pic,
            'addressline_1':customer.address.address_line_1,
            'addressline_2':customer.address.address_line_2,
            'city':customer.address.city,
            'postal_code':customer.address.postal_code,
            'loan_amount':recipt.loan_amount,
            'wig':propert.weight_grams,
            'wimg':propert.weight_milligrams,
            'pvalue':propert.value,
        }
        html_content = template.render(cont)
        return HttpResponse(html_content)

    users = Customer.objects.all()
    return render(request, 'makerec.html', {"users":users})


def viewrec(request,cid,pid):
    template = get_template('reciept.html')
    customer = Customer.objects.get(pk=cid)
    propert = Property.objects.get(pk=pid)
    recipt = Reciept.objects.get(customer=customer,property=propert)
    if request.method=='GET':
        cont ={
            'name':customer.name,
            'age':customer.age,             
            'phone':customer.address.phone,
            'property':propert.name,
            'date':recipt.when,
            'image':customer.pic,
            'addressline_1':customer.address.address_line_1,
            'addressline_2':customer.address.address_line_2,
            'city':customer.address.city, 
            'postal_code':customer.address.postal_code,
            'loan_amount':recipt.loan_amount,
            'wig':propert.weight_grams,
            'wimg':propert.weight_milligrams,
            'pvalue':propert.value,
        }

        html_content = template.render(cont)

        return HttpResponse(html_content)


def dispReceipts(request):
    if request.method == "GET":
        customer_name = request.GET.get('customer_name', '')
        receipts = Reciept.objects.filter(customer__name__icontains=customer_name)
        return render(request, 'displayReceipts.html', {'receipts': receipts, 'searched_name': customer_name}) 



def user_details(request):
    users = Customer.objects.all()
    return render(request, 'user_details.html', {'users': users})

def user_details_individual(request, user_id):
    user = get_object_or_404(Customer, pk=user_id)
    context = {'user': user}
    return render(request, 'individual_user.html', context)

def loan_deat(request,rid):
    reciept = Reciept.objects.get(pk=rid)
    return render(request,'loan_details.html',{"reciept":reciept})

