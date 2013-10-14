from django.conf.urls import patterns, include, url
from django.conf import settings
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LVD.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'player.views.index', name='index'),
    #url(r'^player(?P<video>.*)$', 'player.views.player', name='player'),
    url(r'^(?P<place>[^/]*)(/player)?(?P<video>.*)$','player.views.advancedPlayer',name='advancedplayer'),

)
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)

