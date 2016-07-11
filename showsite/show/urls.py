from django.conf.urls import url

from . import views


app_name = 'show'
urlpatterns = [
	url(r'index', views.index, name='index'),
	url(r'list', views.list_options, name='list'),
	url(r'show', views.show_conf, name='show'),
	url(r'compare_run', views.compare_run, name='compare_run'),
	url(r'logout', views.logout_view, name='logout_view'),
	url(r'(?P<file_name>.+)', views.file_show, name='file_show'),

]