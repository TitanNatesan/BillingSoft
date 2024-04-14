# views.py
import random
from .models import Property, Customer, Address, Loan, Due
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.template import loader
from django.http import HttpResponse
from django.db import transaction
from django.template.loader import get_template
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def home(request):
    return render(request, 'home.html', {})

# def viewrec(request,cid,pid):
#     template = get_template('reciept.html')
#     customer = Customer.objects.get(pk=cid)
#     propert = Property.objects.get(pk=pid)
#     recipt = Reciept.objects.get(customer=customer,property=propert)
#     if request.method=='GET':
#         cont ={
#             'name':customer.name,
#             'age':customer.age,             
#             'phone':customer.address.phone,
#             'property':propert.name,
#             'date':recipt.when,
#             'image':customer.pic,
#             'addressline_1':customer.address.address_line_1,
#             'addressline_2':customer.address.address_line_2,
#             'city':customer.address.city, 
#             'postal_code':customer.address.postal_code,
#             'loan_amount':recipt.loan_amount,
#             'wig':propert.weight_grams,
#             'wimg':propert.weight_milligrams,
#             'pvalue':propert.value,
#         }

#         html_content = template.render(cont)

#         return HttpResponse(html_content)


def calculate_emi(principal, monthly_interest_rate, months):
    principal = float(principal)
    monthly_interest_rate = float(monthly_interest_rate)
    months = int(months)
    r = monthly_interest_rate
    n = months
    emi = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
    return emi

def calculate_emi_components(principal, monthly_interest_rate, tenure_months):
    # Convert monthly interest rate to decimal
    monthly_interest_rate_decimal = monthly_interest_rate / 100.0

    # Calculate EMI using the formula
    emi = (principal * monthly_interest_rate_decimal * (1 + monthly_interest_rate_decimal) ** tenure_months) / \
          ((1 + monthly_interest_rate_decimal) ** tenure_months - 1)

    emi_components = []
    remaining_principal = principal
    total_payable = 0  # Initialize total payable amount

    for month in range(1, tenure_months + 1):
        interest = remaining_principal * monthly_interest_rate_decimal
        principal_payment = emi - interest
        total_payable += emi  # Add current month's EMI to total payable
        remaining_principal -= principal_payment
        emi_components.append((month, emi, principal_payment, interest, remaining_principal))

    return emi_components, total_payable

@transaction.atomic
def makeReciept(request):
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
            )
            address.save()
            customer = Customer(
                name=customer_name,
                age=customer_age,
                pic=customer_pic,
                address=address,
                phone=customer_phone,
            )
            customer.save()

        customer.properties.add(propert)
        customer.save()
        loan_amount = request.POST.get('loan_amount')
        interest_rate = request.POST.get('interest_rate')
        total_dues = request.POST.get('total_dues')
        loan = Loan(
            user = customer,
            property = propert,
            loan_amount = loan_amount,
            intrest_rate = interest_rate,
            no_of_dues = total_dues,
            loan_repaid = 0
        )
        loan.save()
            
        emi_components, total_payable = calculate_emi_components(float(loan.loan_amount), float(loan.intrest_rate), int(loan.no_of_dues))
        loan.total_payable = total_payable
        loan.save()
            
        for month, emi, principal_payment, interest, remaining_principal in emi_components:
            due = Due(
                loan = loan,
                due_status = "pending",
                due_amount = emi,
                paid_amount = 0,
                due_date = loan.when + relativedelta(months=(month)),
                nth_due = month,
                int_due = interest,
                pri_due = principal_payment,
            )
            due.save()
            loan.dues.add(due)
            loan.save()
            
        template = get_template('reciept.html')
        cont ={
            'name':loan.user.name,
            'age':loan.user.age,
            'phone':loan.user.phone, 
            'property':loan.property.name,
            'date':loan.when,
            'image':loan.user.pic,
            'addressline_1':loan.user.address.address_line_1,
            'addressline_2':loan.user.address.address_line_2,
            'city':loan.user.address.city,
            'postal_code':loan.user.address.postal_code,
            'loan_amount':loan.loan_amount,
            'wig':loan.property.weight_grams,
            'wimg':loan.property.weight_milligrams,
            'pvalue':loan.property.value,
        }
        html_content = template.render(cont)
        return HttpResponse(html_content)

    users = Customer.objects.all()
    return render(request, 'makerec.html' , {"users":users})

def dispCustomers(request):
    if request.method == "GET":
        customer_name = request.GET.get('customer_name', '')
        customers = Customer.objects.all()
        return render(request, 'displayCustomers.html', {'customers': customers, 'searched_name': customer_name}) 

def user_details_individual(request, user_id):
    user = get_object_or_404(Customer, pk=user_id)
    context = {'user': user}
    return render(request, 'individual_user.html', context)

def property_details_individual(request, pid):
    property = get_object_or_404(Property, pk=pid)
    context = {'property': property}
    return render(request, 'individual_property.html', context)

def loan_details_individual(request, lid):
    if request.method == "POST":
        due_id = int(request.POST.get('due_id'))
        due = Due.objects.get(pk=due_id)
        paid_amount = float(request.POST.get('paid_amount'))
        payment_mode = request.POST.get('payment_mode')
        due.payment_mode = payment_mode
        due.paid_amount = paid_amount
        due.due_status = "partially_paid" if float(paid_amount) < float(due.due_amount) else "Paid"
        due.paid_date = datetime.now()
        due.save()
        
        loan = due.loan
        rp = float(loan.loan_repaid) + float(paid_amount)
        loan.loan_repaid = rp
        loan.save()
    loan = get_object_or_404(Loan, pk=lid)
    context = {'loan': loan}
    return render(request, 'individual_loan.html', context)

def updateDues(request):
    if request.method == "POST":
        due_id = int(request.POST.get('due_id'))
        due = Due.objects.get(pk=due_id)
        paid_amount = float(request.POST.get('paid_amount'))
        payment_mode = request.POST.get('payment_mode')
        due.payment_mode = payment_mode
        due.paid_amount = paid_amount

        # Check if due date month matches current month
        current_month = datetime.now().month
        due_date_month = due.due_date.month
        # if current_month != due_date_month:
        #     message = f"Cannot update due: Due date month does not match current month"
        #     return JsonResponse({'success': False, 'message': message})

        due.due_status = "partially_paid" if float(paid_amount) < float(due.due_amount) else "Paid"
        due.paid_date = datetime.now()
        due.save()
        
        loan = due.loan
        rp = 0.0
        for d in loan.dues.all():
            rp += float(d.paid_amount)
        loan.loan_repaid = rp
        loan.save()
        return JsonResponse({'success': True, 'message': "Successfully Updated!!!"})

        