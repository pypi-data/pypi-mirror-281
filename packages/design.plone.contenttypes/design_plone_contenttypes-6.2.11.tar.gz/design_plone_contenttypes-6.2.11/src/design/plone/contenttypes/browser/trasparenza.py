# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView


class TrasparenzaView(BrowserView):
    """ """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return


class DettagliProcedimentiView(BrowserView):
    """ """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return
