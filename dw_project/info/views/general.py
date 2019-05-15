import datetime
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from dwapi import datawiz


class GeneralView(View):

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
            data = {
                'date_from': date_from,
                'date_to': date_to,
            }

            turnover = dw.get_products_sale(by='turnover', date_from = date_from, date_to = date_to)
            data['turnover'] = {
                'from': round(turnover.sum(axis=1)[0], 2),
                'to': round(turnover.sum(axis=1)[1], 2),
                'percent': round((round(turnover.sum(axis=1)[1], 2) - round(turnover.sum(axis=1)[0], 2)) /
                            max(round(turnover.sum(axis=1)[1], 2), round(turnover.sum(axis=1)[0], 2)) * 100, 2),
                'diff': round(round(turnover.sum(axis=1)[1], 2) - round(turnover.sum(axis=1)[0], 2), 2),
            }

            quantity = dw.get_products_sale(by='qty', date_from = date_from, date_to = date_to)
            data['quantity'] = {
                'from': round(quantity.sum(axis=1)[0], 2),
                'to': round(quantity.sum(axis=1)[1], 2),
                'percent': round((round(quantity.sum(axis=1)[1], 2) - round(quantity.sum(axis=1)[0], 2)) /
                            max(round(quantity.sum(axis=1)[1], 2), round(quantity.sum(axis=1)[0], 2)) * 100, 2),
                'diff': round(round(quantity.sum(axis=1)[1], 2) - round(quantity.sum(axis=1)[0], 2), 2),
            }

            receipts = dw.get_products_sale(by='receipts_qty', date_from=date_from, date_to=date_to)
            data['receipts'] = {
                'from': round(receipts.sum(axis=1)[0], 2),
                'to': round(receipts.sum(axis=1)[1], 2),
                'percent': round((round(receipts.sum(axis=1)[1], 2) - round(receipts.sum(axis=1)[0], 2)) /
                            max(round(receipts.sum(axis=1)[1], 2), round(receipts.sum(axis=1)[0], 2)) * 100, 2),
                'diff': round(round(receipts.sum(axis=1)[1], 2) - round(receipts.sum(axis=1)[0], 2), 2),
            }

            data['average'] = {
                'from': round(data['turnover']['from'] / data['receipts']['from'], 2),
                'to': round(data['turnover']['to'] / data['receipts']['to'], 2),
            }
            data['average'] = {
                'from': data['average']['from'],
                'to': data['average']['to'],
                'percent': round((data['average']['to'] - data['average']['from']) /
                            max(data['average']['to'], data['average']['from']) * 100, 2),
                'diff': round((data['average']['to'] - data['average']['from']), 2),
            }

            messages.add_message(request, messages.INFO, auth)
            return render(request, 'info\general.html', context={'data': data})

        except:
            return redirect('/login/')
