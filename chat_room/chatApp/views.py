from django.shortcuts import render

# Create your views here.
def home(request,*args,**kwargs):
    return render(request=request,template_name='chatApp/home.html')