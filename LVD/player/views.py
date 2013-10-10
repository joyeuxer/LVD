# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

def index(request):
    return HttpResponseRedirect('playerlive')

def player(request,video):
    if video != 'live':
        video = 'uploads/test'+video+'.mp4'
    clips = ('img/beach.jpg','img/clover.jpg','img/dingdang.jpg','img/drop.jpg','img/flower.jpg','img/spring.jpg','img/train.jpg')
    ids = (2,3,4,5,6,7,8)
    data=zip(ids,clips)	
    return render_to_response('player.html', locals(), context_instance=RequestContext(request))
