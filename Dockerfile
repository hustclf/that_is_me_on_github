FROM python:3.6.8-alpine

LABEL maintainer="hustclf@gmail.com" author="hustclf"

# install requirements
RUN pip install that-is-me-on-github==0.0.2

ENTRYPOINT ["that_is_me_on_github"]
