FROM python:3

# This will buffer our output so it will look “normal” within Docker 
ENV PYTHONUNBUFFERED 1
#This will remove .pyc files from our container which is a good optimization.
ENV PYTHONDONTWRITEBYTECODE 1 

# create a directory to store app source code
RUN mkdir /mindfulblog

# Copy the source code into this directory
COPY . /mindfulblog/

# switch to the directory so that everything runs from here
WORKDIR /mindfulblog

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i "s/\r$//" /mindfulblog/entrypoint.sh
RUN chmod +x /mindfulblog/entrypoint.sh 
ENTRYPOINT ["/mindfulblog/entrypoint.sh"]