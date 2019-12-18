FROM quay.io/cdis/rstudio:master


# COPY premade notebook
RUN mkdir /home/rstudio/inflammatory

ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/Inflammatory_RStudio/Gen3AuthHelper.R /home/rstudio/inflammatory
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/Inflammatory_RStudio/Gen3Submission.R /home/rstudio/inflammatory
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/Inflammatory_RStudio/immune_marker.r /home/rstudio/inflammatory
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/Inflammatory_RStudio/readme.txt /home/rstudio/inflammatory

RUN chmod -R 777 /home/rstudio/inflammatory

RUN touch /home/rstudio/inflammatory/Gen3AuthHelper.R
RUN touch /home/rstudio/inflammatory/Gen3Submission.R
RUN touch /home/rstudio/inflammatory/immune_marker.r
RUN touch /home/rstudio/inflammatory/readme.txt
