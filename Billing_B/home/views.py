from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.template import loader
from django.http import HttpResponse



@api_view(['GET'])
def test(request):
    return Response({"word":"Nalla Word"})

# @api_view(['POST'])
def mkcutsmr(request):
    temp = loader.get_template('customer.html')
    
    if request.method == "POST":
        name = request.POST.get('name')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        pic = request.FILES.get('pic')  # Assuming 'pic' is the name of your file input
        
        # Do something with the form data, e.g., save to a model
        print(request)
        
        return HttpResponse("Form submitted successfully")
    context = {} 
    return HttpResponse(temp.render(context,request))
