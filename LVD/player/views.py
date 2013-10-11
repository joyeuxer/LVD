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

#def current_datetime(request):
#    now = datetime.datetime.now()
#    return render_to_response('current_datetime.html', {'current_date': now})
#def showTablePublisher(request):
    #p1 = Publisher(name='Apress', address='2855 Telegraph Avenue',city='Berkeley', state_province='CA', country='U.S.A.',website='http://www.apress.com/')
    #p1.save()
    #p2 = Publisher(name="O'Reilly", address='10 Fawcett St.',city='Cambridge', state_province='MA', country='U.S.A.', website='http://www.oreilly.com/')
    #p2.save()
#    publisher_list = Publisher.objects.all()



def initDB:
    pass

def insertVideo():
    pass

# work way 
#>>> b1= Book(title='my book 1', publisher=p1,publication_date='2013-09-20')
#>>> b1.save()
#>>> b1.authors.add(a1,a2);
                               
