# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from player.models import VideoInfo
from player.models import VideoIntroduction
from player.models import LiveMenu
from django.conf import settings
import time

def index(request):
    return HttpResponseRedirect('us_playerlive')

def getDate():
    return time.strftime("%Y-%m-%d")


def player(request,video):
    ids=[]
    clips=[]
    if video != 'live':
        try:
            curVideo = VideoInfo.objects.get(id=int(video))
        except VideoInfo.DoesNotExist:
            print "Video id"+video+" isn't in the database yet."
        video = settings.RES_URL_HEAD + curVideo.url
        thumbnail = settings.RES_URL_HEAD + curVideo.thumbnailsLoc
        try:
           curVideoIntro = curVideo.introduction
        except VideoIntroduction.DoesNotExist:
            print "Can not found video info for"+curVideo.name
        #curActors = join(curVideoIntro.actors.all().values())
        #curVideoDesc = "Director: "+curVideoIntro.director+"\n\nContent: "+curVideoIntro.content
        curVideoName = curVideo.name
        curVideoDirector = curVideoIntro.director
        curVideoDesc = curVideoIntro.content
    if video == 'live':
        curDate = getDate().strip()
        print 'cur date = ', curDate
        try:
            todayLiveMenu = LiveMenu.objects.filter(date='2013-10-11')
        except:
            print "Can not get today live memu list"
    try:
        VideoAll = VideoInfo.objects.all()
    except VideoInfo.DoesNotExist:
        print "no video in the database yet."
    for v in VideoInfo.objects.all():
        clips.append(v.thumbnailsLoc)
        ids.append(v.id)
#    clips = ('img/beach.jpg','img/clover.jpg','img/dingdang.jpg','img/drop.jpg','img/flower.jpg','img/spring.jpg','img/train.jpg')
#    ids = (2,3,4,5,6,7,8)
    data=zip(ids,clips)
    return render_to_response('player.html', locals(), context_instance=RequestContext(request))


def advancedPlayer(request,place='us',video=''):
    ids=[]
    clips=[]
    placeMap={ 'us':'America','jk':'','cn':'China','gt':'','ind':'','other':'' }
    print 'Now video = %s ,place = %s.' %(video,place)
    if video != 'live':
        curVideo = ''
        try:
            curVideo = VideoInfo.objects.get(id=int(video))
        except ValueError, VideoInfo.DoesNotExist:
            print "Video id  "+video+" isn't in the database yet."
        if not curVideo:
            try:
                tmpList = searchByPlace(placeMap[place])
                if tmpList:
                     curVideo = tmpList[0]
                else:
                    tmpList = VideoInfo.objects.all()
                    if tmpList:
                        curVideo = tmpList[0]
            except:
                pass
        if curVideo:
            try:
                curVideoIntro = curVideo.introduction
            except VideoIntroduction.DoesNotExist:
                print "Can not found video info for"+curVideo.name
            #curActors = join(curVideoIntro.actors.all().values())
            #curVideoDesc = "Director: "+curVideoIntro.director+"\n\nContent: "+curVideoIntro.content
            curVideoName = curVideo.name
            curVideoDirector = curVideoIntro.director
            curVideoDesc = curVideoIntro.content
            video = settings.RES_URL_HEAD + curVideo.url
            thumbnail = settings.RES_URL_HEAD + curVideo.thumbnailsLoc
    else:
        curDate = getDate().strip()
        print 'cur date = ', curDate
        try:
            todayLiveMenu = LiveMenu.objects.filter(date='2013-10-11')
        except:
            print "Can not get today live memu list"

    try:
        searchedVideoList = searchByPlace(placeMap[place])
    except KeyError, VideoInfo.DoesNotExist:
        print "No video with specified search condition  in the database yet."
    #assert False
    for v in searchedVideoList:
        clips.append(v.thumbnailsLoc)
        ids.append(v.id)
    data=zip(ids,clips)
    return render_to_response('advancedplayer.html', locals(), context_instance=RequestContext(request))



def initDB():
    clearAllTablesRecords()
    insertVideo(name='video1',place='china',url='www.baidu.com',classificationStrList=['horrific','love'], director='xu zheng',actorsNameList=['xu zheng','fenggong'],content='This is a video of xu zheng.')
    insertVideo(name='video2',place='china',url='www.baidu.com',classificationStrList=['comedy','love'], director='feng xiao gang',actorsNameList=['xufan','fenggong'],content='This is a video of feng xiao gang.')
    insertVideo(name='video3',place='china',url='www.baidu.com',classificationStrList=['action','love'], director='feng xiao gang',actorsNameList=['xufan','fenggong'],content='This is a video of feng xiao gang.')

def clearAllTablesRecords():
    Actor.objects.all().delete()
    VideoIntroduction.objects.all().delete()
    Classification.objects.all().delete()
    VideoInfo.objects.all().delete()


#parameter examples: classificationStrList=['a','b','c'], actorsNameList=['sam','tom','kitty']
def insertVideo(name,place='',score='',releaseDate='2013-09-20',thumbnailsLoc='',url='',classificationStrList=[],director='',actorsNameList=[],sex='',birth='1900-01-01',country='',content=''):
    tmpVideo = VideoInfo(name=name,place=place,score=score,releaseDate=releaseDate,thumbnailsLoc=thumbnailsLoc,url=url)
    #create VideoIntroduction object, it can no be null
    if director or content or actorsNameList:
        tmpVideoIntro = VideoIntroduction(director=director,content=content)
        tmpVideoIntro.save()
        if actorsNameList:
            for actorNameStr in actorsNameList:
                targetActorList = Actor.objects.filter(name = actorNameStr)
                # new actor 
                if not targetActorList:
                    tmpActor = Actor(name=actorNameStr,sex=sex,birth=birth,country=country)
                    tmpActor.save()
                    tmpVideoIntro.actors.add(tmpActor)
                # existing actor
                else:
                    tmpVideoIntro.actors.add(targetActorList[0])
        tmpVideo.introduction = tmpVideoIntro
    tmpVideo.save()

    #create Classification object
    if classificationStrList:
        for classificationStr in classificationStrList:
            targetClassificationList = Classification.objects.filter(name = classificationStr)
            # new classification
            if not targetClassificationList:
                tmpClassification = Classification(name=classificationStr)
                tmpClassification.save()
                tmpVideo.classification.add(tmpClassification)
            # existing classification
            else:
                tmpVideo.classification.add(targetClassificationList[0])



def searchByClassification(aimClass):
    aimClassificationList = Classification.objects.filter(name=aimClass)
    allVideoInfoList = VideoInfo.objects.order_by('-score') #ordering from high score to low
    searchedClassifiedVideoList = []
    # No classification record for the aimClass
    if aimClassificationList:
        for video in allVideoInfoList:
            if aimClassificationList[0] in video.classification.all():
                searchedClassifiedVideoList.append(video)

    return searchedClassifiedVideoList


def searchByPlace(aimPlace):
    searchedPlaceVideoList = VideoInfo.objects.filter(place=aimPlace).order_by('-score') #ordering from high score to low
    return searchedPlaceVideoList


