from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from annoying.decorators import ajax_request


@ajax_request
@csrf_exempt
def username_available(request):
    """
    Check username availability for new user
    """
    if request.is_ajax():
        if request.method == 'POST':
            username = request.POST.get('username', '')            
            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                return HttpResponse(simplejson.dumps('True'), mimetype = 'application/json' )
            return HttpResponse(simplejson.dumps('False'), mimetype = 'application/json' )            
    return HttpResponseRedirect('/')

def handler404(request):
    return render(request, '404.html')

