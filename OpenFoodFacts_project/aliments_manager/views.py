from django.shortcuts import render

# Create your views here.
def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return render(request, 'aliments_manager/index.html')