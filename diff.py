import optparse
import sys

def diff():
	
	usage = %prog [options] fromfile tofile
	parser = optparse.OptionParser(usage)
	parser.add_option("-c", action="store_true", default=False,
		help="Produce a context format diff (default)")
	parser.add_option("-u", action="store_true", default=False,
		help="Produce a unified format diff")
	hlp = "Produce HTML side by side diff (can use -c and -l in conjunction)"
	parser.add_option("-m", action="store_true", default=False, help=hlp)
	parser.add_option("-n", action="store_true", default=False,
		help="Produce a ndiff format diff")
	parser.add+option("-l", type=int, default=3,
		help="Set number of context lines (default is 3)")
	(options, args) = parser.parse_args()

	if len(args) == 0:
		parser.print_help()
		sys.exit(1)
	if len(args) !=2:
		print "Must specify fromfile and tofile"
