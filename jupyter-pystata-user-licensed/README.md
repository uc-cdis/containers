## Stata Workspaces

---

### About
 Stata is a proprietary statistical computing language with many research applications. Gen3 Stata workspaces support Stata18 through Jupyter notebooks and Stata's [Python interoperability package](https://pypi.org/project/stata-setup/).

### Images
Since Stata is proprietary software, we do not include any of its components under version control, but instead under a protected S3 bucket. This requires that our images not be built with standard Quay hooks, but rather with a Github workflow, `push_stata_image`, which bundles Stata software into an image and pushes it to `stata-heal:{branch}` on Quay.

Note: While we have received permission from Stata to keep these containers public in keeping with our usual practices, the Stata software bundled in these containers should not be used for any purpose outside of our Gen3 workspaces. If you need access to Stata, please reach out to them directly at www.stata.com.


### Licensing
Stata software requires a license to run. As a one-time step, workspace users should add their license files in their persistent workspace storage as `~/pd/stata.lic`. The notebook has a few lines of python code to check for the license file and copy it to the appropriate location so that Stata can recognize it.

### Local development
To build, enter the root directory of this repo and run:
```
docker build -t stata -f jupyter-pystata-user-licensed/Dockerfile ./jupyter-pystata-user-licensed
```
You will need a local copy of `StataNow18Linux64.tar.gz` for the build.

Then, run this container with your license `stata.lic`,
```
docker run -p 8888:8888 -e STATA_LICENSE='<CONTENTS_FROM_THE_STATA.LIC_FILE>' stata
```
