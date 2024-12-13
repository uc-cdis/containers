## Licensed Stata Workspaces

---

For general information about Gen3 Stata workspaces, see the
[Stata workspaces README](https://github.com/uc-cdis/containers/tree/master/jupyter-pystata-user-licensed)

### Licensing

Stata software requires a license to run.
This container waits for a license provided by an external job.
It then runs a script which launces a jupyter notebook, runs its first cell in order to initialize a STATA session, then deletes the license.
This is to prevent the user from accessing the license directly.

The current external job for license distribution is the
[`distribute-licenses-job`](https://github.com/uc-cdis/cloud-automation/blob/master/kube/services/jobs/distribute-licenses-job.yaml) in the
[cloud-automation repository](https://github.com/uc-cdis/cloud-automation).

#### License file creation

You will need

* a license PDF from Stata
* access to the Stata `stinit` function

One way to access the Stata function is to exec into a pod that is running Stata,
possibly a user-licensed instance. From the bash shell, invoke the Stata function

```
stinit
```

Follow the instructions and add information from your license PDF.
This will generate a license string. The license string will likely have characters
separated by exclamation marks (!). **Save the string!**

#### License secret creation

The license secret can be managed by [`g3auto`](https://github.com/uc-cdis/cloud-automation/blob/9042162/doc/secrets.md).

Store one or more copies of the license string in the file
`g3auto/stata-workspace-gen3-license/stata_license.txt` in your commons.
Run the secret creation command

```
gen3 secrets sync
```

Verify that your secret has been created

```
kubectl get secret stata-workspace-gen3-license-g3auto
```

### Local development

To build, enter the root directory of this repo and run:
```
docker build -t stata-licensed -f jupyter-pystata-gen3-licensed/Dockerfile .

docker run --name stata-licensed -p 8888:8888 stata-licensed /tmp/wait_for_license.sh --JupyterNotebookApp.base_url=/lw-workspace/proxy/ --JupyterNotebookApp.password='' --JupyterNotebookApp.token=''
```

(You will need a local copy of `StataNow18Linux64.tar.gz`.)

Then, with your license `stata.lic`,

```
docker cp stata.lic stata-licensed:/usr/local/stata18/stata.lic
```
