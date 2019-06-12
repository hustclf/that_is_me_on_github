FROM python:3.6.8-alpine

LABEL maintainer="hustclf@gmail.com" author="hustclf"

# set pip mirror to speed up installation, using aliyun as default.
WORKDIR /root
COPY pip.conf .pip/

# copy source code
WORKDIR /usr/src/that_is_me_on_github
COPY . .

# install requirements
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "that_is_me_on_github.py"]
