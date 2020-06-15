from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import random
from .models import Suggestion

def home(request):
    context = {}
    return render(request, 'suggester/main.html', context)

def query_suggestion(request):
    # Python uses the C way to construct strings which means that the %s will be filled in with the string from the number/string
    # that follows the %.
    # random.randint is a way to generate random number. If the arguments supplied is (a, b), it generates a number n such that
    # a <= n <= b
    print('The GET request is: %s' % (request.GET))
    # Use getlist method here, as .get will only grab the last item in a list of a dict
    # request.GET returns a QueryDict object, which is similar to the Dict object with some difference
    cuisine_type_from_select = request.GET.getlist('cuisineType[]')
    has_visited = request.GET.get('hasVisited')

    print('The cuisine_type_from_select request is: %s' % (cuisine_type_from_select))
    print('The has_visited request is: %s' % (has_visited))

    if has_visited == '0':
        has_visited_filter = [False]
    elif has_visited == '1':
        has_visited_filter = [True]
    else:
        has_visited_filter = [True, False]

    if (cuisine_type_from_select == []):
        cuisine_type_from_select = ['TH', 'CN', 'ID', 'JP', 'MY', 'IN', 'WS', 'DS', 'BR', 'FF', 'KR']

    print('The has_visited_filter is: %s' % (has_visited_filter))
        # The way python does if statements is via the indents
        # In method takes a list or even a string and checks all records if any of them matches the in statements
        # This is similar to the SQL WHERE IN clause
    suggestion_master = Suggestion.objects.filter(cuisine_type__in=cuisine_type_from_select).filter(has_visited__in=has_visited_filter)
    print('Cuisine_type_from_select exists.')

    print('The suggestion_master request is: %s' % (suggestion_master))
    if suggestion_master:
        suggestion = random.choice(list(suggestion_master))
        print('The suggestion is: %s' % (suggestion))
        data = {
            'restaurant_id':suggestion.id,
            'restaurant_name': suggestion.restaurant_name,
            'has_visited': suggestion.has_visited
        }

        print('Suggestion_master is not empty. Returning non-empty data %s' % (data))

    else:
        data = {}
        print('Suggestion_master is empty. Returning empty data %s' % (data))
    # Data returned must be a dict
    return JsonResponse(data)

@csrf_exempt
def save_suggestion(request):
    # Check the POST request
    # .get() method is to search a dict and returns a string of the matching and replaces it with the secondary
    # .get() always returns a string, thus by comparing it to the 'true' string, it will be converted to a boolean
    has_visited = request.POST.get('has_visited', None) == 'true'
    restaurant_id = request.POST.get('restaurant_id', None)

    suggestion = Suggestion.objects.get(id=restaurant_id)

    print(has_visited)
    suggestion.has_visited = has_visited
    suggestion.save()

    print('Data saved into the database is %s' % has_visited)

    return HttpResponse('')
