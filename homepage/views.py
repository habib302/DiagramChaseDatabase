from django.shortcuts import render

# Create your views here.

def homepage(request):
   return render(request, 'homepage/homepage.html')
def homepage(request):
   from django.shortcuts import render
   return render(request, "homepage/homepage.html")
