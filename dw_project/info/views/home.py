from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from dwapi import datawiz


class HomeView(View):

    def get(self, request):

        try:
            storage = get_messages(request)
            auth = None
            for message in storage:
                auth = message
                break
            user = auth.message.split(' ')

            dw = datawiz.DW(user[0], user[1])
            data = dw.get_client_info()

            messages.add_message(request, messages.INFO, auth)
            return render(request, 'info\home.html', context={'data': data})

        except:
            return redirect('/login/')
