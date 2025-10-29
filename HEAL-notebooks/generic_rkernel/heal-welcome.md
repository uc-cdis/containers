# **Welcome to the HEAL Workspace**

**This is your personal workspace. No one else can access the data or files here.**

You can learn more about using the HEAL Workspace in the [HEAL Documentation](https://heal.github.io/platform-documentation/workspaces/).

**The `/pd` folder (find it in the panel on the left) is your persistent drive:**

* Use this folder to store files (notebooks, data files, etc) that you want to use again later. The files you save here will still be available when you come back after terminating your workspace session.
* **Any files you create or add outside of this folder will be lost if they are not moved to the `/pd` before your workspace session terminates**.
* This image has a `/pd` with a storage capacity limit of 10Gi

The folder `/healdata.org` in the `/data` folder will host any data files you have downloaded to the workspace through the [HEAL Discovery Page](https://healdata.org/portal). Move these files to the `/pd` directory if you want to access them again after you terminate your workspace session.

## **Get started with Data Exploration**

Open a new "Launcher" tab by clicking the `+` next to `heal-welcome.html` tab at the top of this document.

From the Launcher tab, you can open: a new, empty Jupyter notebook; open a new code console or terminal window; or, create several types of files (text, Markdown, Python). For notebooks or files \- remember to move the file into the `/pd` drive if you want to access them in a later workspace session.

[Learn how to download data files through the HEAL discovery page](https://heal.github.io/platform-documentation/downloading_files/) in our documentation.

Install software tools by using `pip install` (Python) or `CRAN` (R). If you have a requirements text,  you can install them with `pip install -r requirements.txt`. You can view all pre-installed software packages by opening a terminal window and using the command “pip list”.

Find some examples of analyses that can be done in the HEAL Workspace on the [HEAL Example Analyses page](https://healdata.org/portal/resource-browser).

If the locally-stored files you wish to analyze are large in number and/or size, you may need to zip them before uploading to a workspace. Once in a workspace, files can be unzipped using the python library [zipfile](https://docs.python.org/3/library/zipfile.html).

**Note:** The Generic Jupyter Lab image is currently sized for small analyses and testing. The maximum storage in the `/pd` for this image (including any notebooks or tools installed) is 10Gi. If you need a larger image for your analyses, please reach out to the HEAL Data Platform support team at [heal-support@gen3.org](mailto:heal-support@gen3.org) to discuss the possibility of a larger image.

## **Funding a persistent paymodel**

To learn how to fund your workspace after your trial period ends, visit our documentation on [persistent paymodels](https://heal.github.io/platform-documentation/workspaces/heal_workspace_registration/#guidelines-for-requesting-extended-access-to-heal-data-platform-workspaces-using-strides).
