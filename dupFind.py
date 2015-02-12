import hashlib
import io
import os
import sys

class Fil:
	def __init__(self, b, p, n):
		self.bytes = b
		self.path  = p
		self.name  = n

def getSize(path):
	s = os.path.getsize(path)
	return str(s)

def findDups( dirname ):
	files = []
	marks = []
	for fname in os.listdir(dirname):
		p = dirname+fname
		b = getSize(p)
		v = Fil(b,p,fname)
		files.append(v)
	files = sorted(files,key=lambda fil: fil.bytes)
	prev = 0
	for curr in files:
		if(prev == 0):
			prev = curr
			continue
		if(curr.bytes == prev.bytes):
			mp = hashlib.md5()
			mc = hashlib.md5()
			fp = io.FileIO(prev.path,'r')
			fc = io.FileIO(curr.path,'r')
			mp.update(fp.read())
			mc.update(fc.read())
			dp = mp.hexdigest()
			dc = mp.hexdigest()
			if (dc == dp):
				print"DupFind.py:",curr.name,"and",prev.name,"are duplicate files."
				marks.append(curr)
		prev = curr
	for m in marks:
		os.rename(m.path,dirname+"/dups/"+m.name)
	return

def main():
	if (len(sys.argv) < 2):
		print "dupFind.py:\n\tUsage: dupFind.py DIR_PATH"
		return
	dir = sys.argv[1]
	if not os.path.exists(dir):
		print "dupFind.py: ",dir," does not exist!"
		return
	if not os.path.exists(dir+"dups/"):
		os.makedirs(dir+"dups")
	print "dupFind.py: Checking",dir,"for duplicate files..."
	findDups(dir)
	return

main()
