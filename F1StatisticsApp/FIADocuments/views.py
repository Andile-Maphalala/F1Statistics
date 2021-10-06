from django.shortcuts import render
from .models import DocClass
from django.http import HttpResponse, HttpResponseRedirect
import threading
from django_heroku.core import settings
from Head2Head.forms import CheckForm
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Create your views here.

def FIAAdmin(request):
    GetAllData()
    return render(request,'FIADocuments/Data.html')




#////////////////////////////////////// Load Data //////////////////////////////////////////////////////////  

def LoadData(request):
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            Password = form.cleaned_data['pw']
            if Password == settings.MYPASSWORD:
                # LoadDrivers()
                #multithreading as a workaround for the timeout issues in deployment
                # t = threading.Thread(target=LoadRaceWeekendData)
                # t.setDaemon(True)
                # t.start()
                return HttpResponseRedirect('load')
                
            else:
                url = 'load?value=False'
                return HttpResponseRedirect(url)
        else:
            url = 'load?value=Form'
            return HttpResponseRedirect(url)

# def GetAllData():
#     AllLinks = GetLinks()
#     for currentLink in AllLinks:
#         print('Starting with ' +currentLink)
#         GetDocuments('https://www.fia.com' + currentLink)
#         print('Done with ' +currentLink)
        
#     print('Done')



def GetDocuments():
    ListOfDocmumentsClass = []
    page = requests.get('https://www.fia.com/documents/fia-formula-one-world-championship-14')
    soup = BeautifulSoup(page.content, 'html.parser')

    Events = soup.find_all("ul", attrs={"class": "event-wrapper"})


    for x in Events:
        GP = x.find("div", attrs={"class": "event-title"}).text
        print("Starting with " + GP)
        ListOfDoc = x.find_all("li",attrs={"class": "document-row" })
        for z in ListOfDoc:
            child = z.find("a")
            url = child.get("href")
            LinkChild =child.findChildren()
            title = child.find("div", attrs={"class": "title"}).text.replace('\n', ' ').strip()
            if title != '':
                published = child.find("span", attrs={"class": "date-display-single"}).text.replace('\n', ' ').strip()
                index = published.index(' ')
                if published[index -1] == '.':
                    DateUploaded = datetime.strptime(published, '%d.%m.%y. %H:%M')
                else:
                    DateUploaded = datetime.strptime(published, '%d.%m.%y %H:%M')

                CurrentDocument =  DocClass()
                CurrentDocument.GP = GP
                CurrentDocument.Title = title
                CurrentDocument.Url = 'https://www.fia.com' + url
                stringdate = str(DateUploaded.year) + '-' + str(DateUploaded.month) +'-' + str(DateUploaded.day) +' ' + str(DateUploaded.hour)+ ':'+ str(DateUploaded.minute) + ':'+ str(DateUploaded.second)
                CurrentDocument.date = DateUploaded

                CurrentDocument.save()


    return ListOfDocmumentsClass