from django.shortcuts import render

# Create your views here.







def editor_page(request):
   from django.shortcuts import render
   return render(request, "quiver_editor/editor_page.html")
