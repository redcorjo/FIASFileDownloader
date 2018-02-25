import sys
import os
import pydoc
import re

mybasedir = "../src"
mydocsdir = "../docs"
myfile = "FIASFileDownloader.html"

sys.path.append(mybasedir)
pydoc.writedocs(mybasedir)

with open(myfile) as f:
    content = f.read()

if os.path.exists(myfile):
    os.rename(myfile, mydocsdir + "/" + myfile)

myregex = re.findall(r'(?<=<a href=")([^"]*).html', content)

for mymodule in myregex:
    pydoc.writedoc(mymodule)
    mydochtml = mymodule + ".html"
    if os.path.exists(mydochtml):
        os.rename(mydochtml, mydocsdir + "/" + mydochtml)

print "Process completed"