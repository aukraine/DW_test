import datetime
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from dwapi import datawiz


class DownView(View):

    def get(self, request):

        try:
            storage = get_messages(request)
            auth = None
            for message in storage:
                auth = message
                break
            user = auth.message.split(' ')

            dw = datawiz.DW(user[0], user[1])
            date_from = datetime.date(2015, 11, 17)
            date_to = datetime.date(2015, 11, 18)
            turnover = dw.get_products_sale(by='turnover', date_from = date_from, date_to = date_to)
            quantity = dw.get_products_sale(by='qty', date_from = date_from, date_to = date_to)

            ids = list(turnover)
            quantity_from = list(quantity.iloc[0])
            quantity_to = list(quantity.iloc[1])
            turnover_from = list(turnover.iloc[0])
            turnover_to = list(turnover.iloc[1])
            data = [[dw.get_product(products=ids[i])['product_name'], round(quantity_to[i] - quantity_from[i], 2), round(turnover_to[i] - turnover_from[i], 2)]
                    for i in range(len(ids)) if quantity_from[i] > quantity_to[i]]

            messages.add_message(request, messages.INFO, auth)
            return render(request, 'info\down.html', context={'data': data})

        except:
            return redirect('/login/')
