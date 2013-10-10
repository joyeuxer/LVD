# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

def index(request):
    return HttpResponseRedirect('playerlive')

def player(request,video):
    if video != 'live':
        video = 'uploads/test'+video+'.mp4'	
    return render_to_response('player.html', locals(), context_instance=RequestContext(request))
