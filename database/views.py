from django.shortcuts import render
from .memgraph_conn import get_memgraph
from .models import *

# Create your views here.

def test_memgraph(request):
   mg = get_memgraph(request)
   
   D = Diagram(name="My Diagram").save(mg)
   X = D.create_object(latex="X", mg=mg)
   
   #mg.save_relationship(f)
   
   return render(request)
   
