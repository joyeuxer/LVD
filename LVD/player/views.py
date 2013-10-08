# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

def player(request):
    return render_to_response('player.html', locals(), context_instance=RequestContext(request))
