from django.shortcuts import render

# Create your views here.

def cd_editor(request):
   return render(request, 'cd_editor.html')