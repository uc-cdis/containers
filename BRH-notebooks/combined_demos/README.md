# Biomedical Research Hub (BRH) workspace README

Welcome to the BRH workspace! Here you will find many different tutorial python notebooks that you can run to familiarize yourself with the BRH mesh -- the available data and analysis tools.  This README will provide some basic background information useful for running these notebooks. Make sure to also review the "Guideline to get started in Workspaces" in BRH Documentation [here](https://brh.data-commons.org/dashboard/Public/index.html#GuidelineToGetStarted) that describes how to get started with analyses in workspaces


### Login and authorization
Please see [Login in BRH Documentation](https://brh.data-commons.org/dashboard/Public/index.html#LoginPage) . You will need to login to obtain authorization and access to access studies and perform analyses in workspaces


### Workspace organization

In the workspace, you will see two directories in addition to python notebooks: 1) `pd`, 2) `work`. pd stands for persistent drive. You can save your code, plots, or any other analyses files in `pd`. This will persist after the workspace is terminated. Do not save any files in `pd/data`. Any project files you export from the Discovery page lives here, so this folder is specifically for hosting those data files. `work` directory can be used to store code and analysis plots. However, these will not be persistent when you `Terminate Workspace`.

### Terminal

You can launch a new terminal session by clicking File->Terminal. You can see the current working directory is `/home/jovyan`. This is where the directories `pd` and `work`, and other python notebooks live. When you download any data files for a project using the Gen3 software, they will be downloaded in `/home/jovyan`.


### Notebooks

Notebooks ending in .ipynb are standard jupyter notebooks. You can select a cell and run it to learn about each step. If you have never ran jupyter notebooks before, please see https://jupyter.org/ to get started.  The notebook `data_access_how_to.ipynb` provides an introduction to different ways of accessing data in the BRH workspace. Make sure to check that one out, if you are new to this workspace. All .ipynb notebooks pull data using one or more of the methods listed in `data_access_how_to.ipynb`.

### README.md

This file you are viewing is a README markdown file which can be rendered by jupyter notebooks in the correct format. To view it in the markdown format right click on `README.md` file on the left panel where all the .ipynb are listed. Then select `Open With-> Markdown Preview`.


### Controlled access and open access notebooks

Both controlled access and open access data are presented in this workspace. The two notebooks that use controlled access data are `ACTT1_accessclinical.ipynb` and `JCOIN_Tracking_Opioid_Stigma.ipynb`. You need access to these studies to be able to run these notebooks.


### Gen3 and GUIDs

To pull data files for a project, the notebooks use the Gen3 software, an open source software developed and maintained at the Center for translational data science, University of Chicago. Gen3 allows users to access and explore data and metadata files associated with projects in a cloud agonistic manner. This is achieved by accessing a file object using its Globally unique identifier (GUID), which is a unique identifier associated with the file. An example GUID looks like `dg.6VTS/342e89bd-3d37-49be-8f97-ffb283649b9a`.

### Further Readings
[Gen3 API's](https://docs.gen3.org/gen3-resources/user-guide/using-api/)
[JupyterLab Documentation](https://jupyterlab.readthedocs.io/en/stable/)

### Have a question? Please Contact Technical Support
[Technical Support](support@gen3.org)

