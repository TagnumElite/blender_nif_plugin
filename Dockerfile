FROM ubuntu:xenial

RUN apt-get update && \
	apt-get install -y \
		curl \
		bzip2 \
		libfreetype6 \
		libgl1-mesa-dev \
		libglu1-mesa \
		libxi6 \
		libxrender1 && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

ENV BLENDER_VERSION 2.80
ENV BLENDER_HOME /usr/local/blender
ENV BLENDER_ADDONS $BLENDER_HOME/$BLENDER_VERSION/scripts/addons
ENV BLENDER_DL_URL http://mirror.clarkson.edu/blender/release/Blender$BLENDER_VERSION/blender-$BLENDER_VERSION-linux-glibc217-x86_64.tar.bz2

RUN mkdir $BLENDER_HOME && \
	curl -SL "$BLENDER_DL_URL" -o blender.tar.bz2 && \
	tar -jxvf blender.tar.bz2 -C $BLENDER_HOME --strip-components=1 && \
	rm blender.tar.bz2
