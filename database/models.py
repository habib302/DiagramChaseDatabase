from .memgraph_conn import get_memgraph
from DiagramChaseDatabase.settings import MAX_LATEX_LENGTH

mg = get_memgraph()

class Model:  
   query = None
   
   @property
   def node_type(self):
      return self.__class__.__name__   
   
class Class(Node):
   def __init__(self):
      self.

class Ob(Class):
   def __init__(self, cat:Category):
      

class Ob(Class):
   def __init__(self, str):
      
A in Ob("C")





