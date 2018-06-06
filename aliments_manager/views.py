from .functionnalities import Functionnalities
from django.shortcuts import render, redirect
from .forms import ContactForm, RegistrationForm, ConnectionForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from aliments_manager.models import Favorites


# Create your views here.
def home(request):
    """
    view displaying the main page except if the user fill the form correctly and submit it
    he will be redirected to the results view.
    """
    choice = Functionnalities.searchFormValid(request)
    if choice[0] == "redirect":
        return redirect(choice[1])
    else:
        return render(request, 'aliments_manager/index.html', {"search":choice[0]})

def results(request, aliment_searched, page_id):
    """
    This view display the results of the user searched made from the search form.
    """
    previous_session = Functionnalities.updateSession(request)
    context = Functionnalities.getAlimentsFromAPI(request, previous_session, aliment_searched, page_id)

    """
    Those 5 lines of code below which appears in most views just redirect the user to 
    the results view with the content of the form filled in the navbar
    """
    choice = Functionnalities.searchFormValid(request)
    if choice[0] == "redirect":
        return redirect(choice[1])
    else:
        context["search"] = choice[0]

    return render(request, 'aliments_manager/results.html', context)

def registration(request):
    """
    View displaying a form to register when called
    """
    choice = Functionnalities.searchFormValid(request)
    if choice[0] == "redirect":
        return redirect(choice[1])

    """
    If the registration form is valid, the view check if the user is already in db.
    If it s the case, the registration page is loaded with an error message saying
    that the account already exist, otherwise the user is sent to the connection page
    with a message indicating that he registered successfully.
    """
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.cleaned_data['nameUser']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        user_exist = User.objects.filter(username=user)
        if user_exist:
            context = {"error_msg": "Désolé mais ce compte existe déjà", "form": form, "error":True}
            return render(request, 'aliments_manager/registration.html', context)
        else:
            newUser = User.objects.create_user(user, email, password)
            return redirect('connection')

    context = {"form":form, "search":choice[0]}
    return render(request, 'aliments_manager/registration.html', context)

def connection(request):
    """
    View displaying a form used to connect on your personnal account
    """
    choice = Functionnalities.searchFormValid(request)
    if choice[0] == "redirect":
        return redirect(choice[1])

    """
    When the user fill the form to connect, an error message is displayed in case of
    failure, or the user is redirect to the home page with a message of success
    """
    form = ConnectionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.cleaned_data['nameUser']
            password = form.cleaned_data['password']
            user = authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                context = {"error":True, "form":form, "search":choice[0]}
                return render(request, 'aliments_manager/connection.html', context)
    else:
        context = {"form":form, "search":choice[0]}
        return render(request, 'aliments_manager/connection.html', context)

def disconnection(request):
    """
    View used to disconnet.It redirects on the main page once done.
    """
    logout(request)
    return redirect(reverse(home))

def account(request):
    """
    View used to display the account informations
    """
    choice = Functionnalities.searchFormValid(request)
    if choice[0] == "redirect":
        return redirect(choice[1])

    #If the user isn't connected, he s redirect to the connection view
    #else, the informations or displayed
    user = str(request.user)
    if user == "AnonymousUser":
        return redirect('connection')
    else:
        return render(request, 'aliments_manager/account.html')

def show_favorites(request, page_id):
    """
    Display the list of favorites aliments saved by the user
    """
    choice = Functionnalities.searchFormValid(request)
    if choice[0] == "redirect":
        return redirect(choice[1])

    #If the user isn't connected, he s redirect to the connection view
    #else, the aliments saved by this user or displayed on the page
    username = request.user.username
    if username == "":
        return redirect('connection')
    else:
        display = Functionnalities.getPage(username, page_id)
        context = {"aliments":display, "search":choice[0]}
        return render(request, 'aliments_manager/favorites.html', context)

@csrf_exempt
def add_favorite(request):
    """
    Add the aliment selected in the database among the favorites of the user connected
    """
    if request.method == 'POST':
        username = request.user.username
        img = request.POST['img']
        text = request.POST['text']
        grade = request.POST['grade']
        code = request.POST['code']
        url = request.POST['url']
        if username == "":
            return JsonResponse({"msg":" Vous devez vous connecter pour enregistrer un aliment en favoris"})
        else:
            user = User.objects.get(username=username)
            print(code)
            in_db = Favorites.objects.filter(user=user).filter(code=code[:13])
            print(in_db)
        if in_db and username:
            print("existe déjà")
            return JsonResponse({"msg":" Cet aliment est déjà dans vos favoris"})
        else:
            print("ajout")
            Favorites.objects.create(user=user, image=img, name=text, nutriscore=grade[-5], code=code, url=url)
            return JsonResponse({"msg":" l'aliment a bien été ajouté"})

def show_aliment(request, code):
    """
    Display the informations about the aliment selected
    """
    context = Functionnalities.getNutrientInfos(code)

    choice = Functionnalities.searchFormValid(request)
    if choice[0] == "redirect":
        return redirect(choice[1])
    else:
        context["search"] = choice[0]

    return render(request, 'aliments_manager/aliment.html', context)

def show_legalmentions(request):
    """
    Display the page containing the legal mentions
    """
    return render(request, 'aliments_manager/legalmentions.html')