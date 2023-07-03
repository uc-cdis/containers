import os.path
import os
import shutil

if os.path.isfile(f"/home/{os.environ['NB_USER']}/pd/stata.lic"):
	shutil.copyfile(f"/home/{os.environ['NB_USER']}/pd/stata.lic", "/usr/local/stata17/stata.lic")
