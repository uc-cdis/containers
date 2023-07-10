## Licensed Stata Workspaces

---

For general information about Gen3 Stata workspaces, see the [Stata workspaces README](https://github.com/uc-cdis/containers/tree/master/jupyter-pystata)

### Licensing
Stata software requires a license to run. This container waits for a license to by provided by an external job, then runs
a script which launces a jupyter notebook and runs its first cell in order to initialize a STATA session, then deletes the license.
This is to prevent the user from accessing the license directly.

The current external job for license distribution is the [`distribute-licenses-job`](https://github.com/uc-cdis/cloud-automation/blob/master/kube/services/jobs/distribute-licenses-job.yaml) in the [cloud-automation repository](https://github.com/uc-cdis/cloud-automation).

### Local development
To build, enter the root directory of this repo and run:
```
docker build -t stata-licensed -f jupyter-pystata-licensed/Dockerfile .

docker run --name stata-licensed -p 8888:8888 stata-licensed /tmp/wait_for_license.sh --NotebookApp.base_url=/lw-workspace/proxy/ --NotebookApp.password='' --NotebookApp.token=''
```

Then, with your license `stata.lic`,

```
docker cp stata.lic stata-licensed:/usr/local/stata17/stata.lic
```
