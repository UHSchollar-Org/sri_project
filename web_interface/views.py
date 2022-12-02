from django.http import HttpRequest, HttpResponse
from django.template import loader
#from source import main

def main_page(request):
    index = loader.get_template('index.html')
    return HttpResponse(index.render({}, request))
    

def response_query(request, query):
    return HttpResponse(query)