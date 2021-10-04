from django.shortcuts import render
from .models import DocClass
from django.http import HttpResponse

# Create your views here.

def FIAAdmin(request):
    Myclass = DocClass()
    Myclass.gp = 'Monaco'
    Myclass.content = 'foo safsgewgwgagq ewfwfrwgeg'
    Myclass.date = '2000-03-01'
    Myclass.url = 'link'
    Myclass.title = 'Ím just testing'
    Myclass.save()
    print("Done")
    return render(request,'FIADocuments/Data.html')