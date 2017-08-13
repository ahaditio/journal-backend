from contextlib import contextmanager
import time

@contextmanager
def tag(name):
    print "<%s>" % name
    yield
    print "</%s>" % name

with tag("h1"):
	time.sleep(5)
	print "andra"