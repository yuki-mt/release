FROM continuumio/miniconda3:4.8.2

RUN apt-get update && apt-get install -y \
  mecab \
  libmecab-dev \
  mecab-ipadic-utf8 \
  make \
  curl \
  sudo \
  g++

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
  && cd mecab-ipadic-neologd \
  && bin/install-mecab-ipadic-neologd -n -y \
  && cd .. \
  && rm -rf mecab-ipadic-neologd

ENV NEOLOGD_DIR /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd

ADD conda.yaml conda.yaml
RUN . /opt/conda/etc/profile.d/conda.sh \
  && conda activate base \
  && conda env update --file conda.yaml

WORKDIR /root/app
