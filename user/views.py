from django.shortcuts import render


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if len(username) > 32 or len(password) > 32 or email > 64:
            pass
