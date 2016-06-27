import optparse
import sys
import os
import difflib
import time
import re
import subprocess

def diff(commands, writefile):

	args = re.split(' ', commands)
	usage = "usage: %prog [options] fromfile tofile"
	parser = optparse.OptionParser(usage)
	parser.add_option("-c", action="store_true", default=False,
		help="Produce a context format diff (default)")
	parser.add_option("-u", action="store_true", default=False,
		help="Produce a unified format diff")
	hlp = "Produce HTML side by side diff (can use -c and -l in conjunction)"
	parser.add_option("-m", action="store_true", default=False, help=hlp)
	parser.add_option("-n", action="store_true", default=False,
		help="Produce a ndiff format diff")
	parser.add_option("-l", "--lines", type=int, default=3,
		help="Set number of context lines (default is 3)")
	(options, args) = parser.parse_args(args)

	if len(args) == 0:
		parser.print_help()
		sys.exit(1)
	if len(args) !=2:
		print "Must specify fromfile and tofile"

	fromfile, tofile = args

	n = options.lines

	fromdate = time.ctime(os.stat(fromfile).st_mtime)
	todate = time.ctime(os.stat(tofile).st_mtime)
	fromlines = open(fromfile, 'U').readlines()
	tolines = open(tofile, 'U').readlines()

	if options.u:
		diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile,
			fromdate, todate, n=n)
	elif options.n:
		diff = difflib.ndiff(fromlines, tolines)
	elif options.m:
		diff = difflib.HtmlDiff().make_file(fromlines, tolines, fromfile, tofile, context=options.c, numlines=n)
	else:
		diff = difflib.context_diff(fromlines, tolines, fromfile, tofile,
			fromdate, todate, n=n)

	with open(writefile, 'w+') as wfile:
		wfile.writelines(diff)

	subprocess.call(["xdg-open", writefile])

args = raw_input("Enter diff: ")
filename = raw_input("Enter writefile name: ")
diff(args, filename)