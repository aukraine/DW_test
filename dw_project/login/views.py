from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages


class LoginView(View):

    def get(self, request):

        return render(request, 'login\login.html')

    def post(self, request):

        try:
            message = request.POST.get('login') + ' ' + request.POST.get('password')
            messages.add_message(request, messages.INFO, message)
            return redirect('/home/')

        except:
            return render(request, 'login\login.html')
