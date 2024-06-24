# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.servizio import IServizio
from plone.indexer.decorator import indexer


@indexer(IServizio)
def service_venue(context, **kw):
    luoghi = getattr(context, "dove_rivolgersi", [])
    return [luogo.UID() for luogo in filter(bool, [x.to_object for x in luoghi])]


@indexer(IServizio)
def canale_digitale_link(context, **kw):
    link = getattr(context, "canale_digitale_link", None)
    return bool(link)
