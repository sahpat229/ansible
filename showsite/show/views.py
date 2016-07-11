from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.staticfiles.views import serve
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import TextFiles
import json
import showCommands
import datetime
import text2html
import re
import logging
import os
import diff
import mimetypes
# Create your views here.

username = ""
privilege = ""

hostname = ""
password = ""
host_user = ""
logged_in = False


def index(request):
	if request.method == 'GET':
		return render(request, 'show/index.html')
	else:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is None:
			context = {'error_msg': "Invalid username or password"}
			return render(request, 'show/index.html', context)
		else:
			login(request, user)
			username = user.username
			response = HttpResponseRedirect(reverse('show:list'))
			return response
@login_required
def list_options(request):
	context = {'privilege': privilege}

	return render(request, 'show/list.html', context)

@login_required
def show_conf(request):
	if request.method == 'GET':
		return render(request, 'show/show.html')
	if request.method == 'POST':
		logger = logging.getLogger(__name__)
		logger.debug("HI")
		if request.POST.has_key('os'):
			os = request.POST['os']
			function = request.POST['function']
			textfile = get_object_or_404(TextFiles, os=os, func=function)
			with open(textfile.lines, 'r') as lines:
				textlines = [line for line in lines]
				return JsonResponse({'lines': textlines})

		else:
			hostname = request.POST['hostname']
			password = request.POST['password']
			host_user = request.POST['username']
			lines = request.POST['lines']
			commands = re.split("\n", lines)
			commands = commands[0:(len(commands) - 1)]
			outputfilename = ""
			items = re.split(' ', str(datetime.datetime.now()))
			for item in re.split(' ', str(datetime.datetime.now())):
				outputfilename = outputfilename + item + "_"
			outputfilename = outputfilename + host_user
			path = '/etc/ansible/showsite/show/show_outputs/'
			showCommands.execute(hostname, host_user, password, 
				commands, path + outputfilename +".txt")
			text2html.text2html(path + outputfilename+".txt", path + outputfilename+".html")
			file = open(path + outputfilename+'.html', 'r')
			response = HttpResponse(file.read(), content_type='text/html')
			response['Content-Disposition'] = 'attachment; filename="foo.html"'
			file.close()
			return response

@login_required
def compare_run(request):
	if request.method == 'GET':
		return render(request, 'show/compare_run.html')
	if request.method == 'POST':
		compare_hostname = ""
		if request.POST.has_key('hostname'):
			compare_hostname = request.POST['hostname']
			matched_items = []
			for item in os.listdir('/etc/ansible/showsite/show/show_outputs'):
				match = compare_hostname + ".txt"
				if re.search(match, item) != None:
					matched_items.append(item)
			return JsonResponse({'matched_items': matched_items})

		else:
			line_total = request.POST['lines']
			lines = re.split('\n', line_total)
			lines = lines[0: (len(lines) - 1)]
			path = '/etc/ansible/showsite/show/show_outputs/'
			path_comp = '/etc/ansible/showsite/show/compare_outputs/'
			outputfilename = ""
			items = re.split(' ', str(datetime.datetime.now()))
			for item in re.split(' ', str(datetime.datetime.now())):
				outputfilename = outputfilename + item + "_"
			outputfilename = "compare" + outputfilename + host_user
			diff.diff(path+lines[0], path+lines[1], path_comp+outputfilename)

			return JsonResponse({'data': outputfilename})

@login_required
def file_show(request, file_name):
	path_comp = '/etc/ansible/showsite/show/compare_outputs/'
	openfile = open(path_comp + file_name, 'r')
	response = HttpResponse(openfile.read())
	openfile.close()
	response['Content-Type'] = 'text/html'
	response['Content-Length'] =  str(os.stat(path_comp+file_name).st_size)
	response['Content-Encoding'] = 'UTF-8'
	response['Content-Disposition'] = 'attachment; ' + 'filename:"output.html"'
	return response

def logout_view(request):
	logout(request)
	return render(request, 'show/logout_success.html')