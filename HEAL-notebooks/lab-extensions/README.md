# JupyterLab with extensions for HEAL


## About

An extension of the Generic JupyterLab environment with common JupyterLab Extensions.



## Building a Notebook

To build this version edit the `requirements.txt` file to add the desired packages and lab extensions and then push to
the `feat/nbbuilder` branch. Some packages such as `lckr-jupyterlab-variableinspector` cannot be added through the
`requirements.txt` file. In this case create a local text file called `lab-extension.Dockerfile` with the following text

```
FROM quay.io/cdis/heal-notebooks:lab-extensions__xxx

RUN pip install lckr-jupyterlab-variableinspector
```

then run `docker build -f lab-extension.Dockerfile .` in your terminal. This will then create a local image
`<image_tag>` which you can add to the lab-extension image by running:

`docker image tag <image_tag> quay.io/cdis/heal-notebooks:lab-extensions__xxx`

`docker push quay.io/cdis/heal-notebooks:lab-extensions__xxx`

Now the lab extension image is ready to be added to your data commons manifest/hatchery file.
