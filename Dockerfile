# Use Blender
FROM ikester/blender:2.79

# ikester/blender entrypoint is blender, we don't need that right away
ENTRYPOINT ["exec"]

# Set the working directory to /plugin
WORKDIR /plugin

# Copy the current directory contents into the container at /plugin
COPY . /plugin

# Download pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o /get-pip.py

# Install Pip to blender built-in python
RUN /usr/local/blender/2.79/python/bin/python3.5m /get-pip.py

# Install any needed packages specified in requirements.txt
RUN /usr/local/blender/2.79/python/bin/python3.5m -m pip install -U -r docs/requirements.txt

# Set BLENDERHOME Env
ENV BLENDERHOME /usr/local/blender

# Build docs
RUN docs/make html

# Run Tests, TODO ACTUALLY RUN TESTS
CMD ["echo", "Hello World"]
