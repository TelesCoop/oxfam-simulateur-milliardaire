FROM public.ecr.aws/lambda/python:3.8


RUN yum -y install inkscape

COPY requirements.txt  .
RUN  pip3 install boto==2.49.0 --target "${LAMBDA_TASK_ROOT}"

RUN mkdir -p /usr/local/share/fonts
COPY OxfamGlobalHeadline.ttf /usr/local/share/fonts/
COPY Oxfam_TSTARPRO-Bold.otf /usr/local/share/fonts/
RUN fc-cache -fv

COPY template.svg ${LAMBDA_TASK_ROOT}

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
