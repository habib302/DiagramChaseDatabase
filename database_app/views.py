from django.shortcuts import render, redirect, HttpResponse
from .models import Object, Category, Diagram, get_model_by_uid, get_model_class, get_unique
from diagram_chase_database.http_tools import get_posted_text
from django.http import JsonResponse
from diagram_chase_database.python_tools import full_qualname
from django.db import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from diagram_chase_database.settings import DEBUG, MAX_USER_EDIT_DIAGRAMS
from neomodel.properties import StringProperty
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.templatetags.static import static
import base64
import json

# Create your views here.

def embed_diagram(request, diagram_id):
   if request.method == 'GET':
      diagram = get_model_by_uid(Diagram, uid=diagram_id)
      data = diagram.quiver_format()
      data = json.dumps(data)
      data = base64.b64encode(data.encode('utf-8'))         
      diagram.embed_data = f'{static("")}/quiver/src/index.html?q={data.decode()}&embed'
      
      context = {
         'diagram' : diagram
      }
      
      return render(request, 'database_app/embed_diagram.html', context)
   


def load_diagram_from_database(request, diagram_id):
   try:
      if request.method == 'GET':
         diagram = get_model_by_uid(Diagram, uid=diagram_id)
         json_str = json.dumps(diagram.quiver_format())
         
         return HttpResponse(json_str, content_type='text/plain; charset=utf8')
      
   except Exception as e:
      return redirect('error', f'{full_qualname(e)}: {str(e)}')


@login_required   
def save_diagram_to_database(request, diagram_id:str):
   try:
      if request.method != 'POST': #or not request.headers.get("contentType", "application/json; charset=utf-8"):
         raise OperationalError('You can only use the POST method to save to the database.')            
      user = request.user.username

      diagram = get_model_by_uid(Diagram, uid=diagram_id)

      if diagram is None:
         raise ObjectDoesNotExist(f'There exists no diagram with uid "{diagram_id}".') 

      if diagram.checked_out_by != user:
         raise OperationalError(
               f'The diagram with id "{diagram_id}" is already checked out by {diagram.checked_out_by}')                

      body = request.body.decode('utf-8')

      if body:
         try:
            data = json.loads(body)                
         except json.decoder.JSONDecodeError:
            # For some reason, empty diagrams are resulting in the body as a URL str (not JSON)
            data = [0, 0]               
      else:
         data = [0, 0]

      diagram.delete_objects()
      diagram.load_from_editor(data)        
      
      messages.success(request, f'🌩️ Successfully saved diagram (id={diagram.uid}) to the database!')

      return JsonResponse(
           'Wrote the following data to the database:\n' + str(data), safe=False)

   except Exception as e:
      #if DEBUG:
         #raise e
      return JsonResponse({'error_msg' : f'{full_qualname(e)}: {str(e)}'})


def test(request):
   return render(request, 'test.html')


def my_diagram_list(request):   
   diagrams = Diagram.nodes.filter(checked_out_by=request.user.username)
   diagram_list = []
   
   for diagram in diagrams:
      data = diagram.quiver_format()
      data = json.dumps(data)
      data = base64.b64encode(data.encode('utf-8'))         
      #diagram.embed_data = f"/static/quiver/src/index.html?q={data.decode()}&embed" 
      diagram.embed_data = data.decode()
      diagram_list.append(diagram)
      
   #page_num %= len(diagrams)
   
   context = {
      'diagrams': diagram_list,
   }
   
   return render(request, "database_app/my_diagram_list.html", context)


@login_required
def diagram_editor(request, diagram_id:str):
   try:
      session = request.session
      user = request.user.username

      if 'diagram ids' not in session:
         session['diagram ids'] = []
      else:
         if diagram_id not in session['diagram ids'] and \
               len(session['diagram ids']) == MAX_USER_EDIT_DIAGRAMS:
            raise OperationalError(f"You can't have more than {MAX_USER_EDIT_DIAGRAMS} diagrams checked out.")

      diagram = get_model_by_uid(Diagram, uid=diagram_id)

      if diagram:
         if diagram.name == '':
            raise ValueError('Diagram name must not be empty.')

         if not diagram.checked_out_by:
            diagram.checked_out_by = user
            session['diagram ids'].append(diagram_id)
            session.save()
         else:
            if diagram.checked_out_by != user:
               raise OperationalError(
                       f'The diagram with id "{diagram_id}" is already checked out by {diagram.checked_out_by}')
      else:
         raise ObjectDoesNotExist(f'There exists no diagram with uid "{diagram_id}".')                

      category = diagram.category.single()

      diagram_data = json.dumps(diagram.quiver_format())

      context = {
         'diagram_name' : diagram.name,
         'category_name' : category.name,
         'category_id' : category.uid,
         'diagram_id' : diagram.uid,
         'quiver_str' : diagram_data,
         'commutes_text' : diagram.commutes_text,
      }

      messages.success(request, f'🌩️ Successfully loaded diagram (id={diagram.uid}) from the database!')
      return render(request, 'database_app/diagram_editor.html', context)  

   except Exception as e:
      messages.error(request, f'{full_qualname(e)}: {str(e)}')   
      return redirect('home')


@login_required
def create_new_diagram(request):   
   diagram = Diagram.our_create(name="Untitled Diagram")
   diagram.checked_out_by = request.user.username
   diagram.save()
   return redirect('diagram_editor', diagram.uid)