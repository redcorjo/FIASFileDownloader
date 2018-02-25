#!/usr/bin/env bash

DOCSDIR="../docs"
PROGRAM="FIASFILEDownloader"
MODULES="rarfile urllib2 os time re argparse"

pydoc -w ../src/${PROGRAM}.py
mv ${PROGRAM}.html ${DOCSDIR}

DOCSDIR="../docs"
MODULES="rarfile urllib2 os time re argparse"

for MODULE in ${MODULES}
do
    pydoc -w ${MODULE}
    mv ${MODULE}.html ${DOCSDIR}
done
