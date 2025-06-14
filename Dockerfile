FROM docker.io/library/python:3.11-alpine
RUN pip install --upgrade pip

WORKDIR /app

# Entry point
ADD entrypoint.sh /
RUN chmod +x /entrypoint.sh

# Download CTY Plist
RUN wget https://www.country-files.com/cty/cty.plist

# Dependecies
ADD requirements.txt /app/
RUN pip install -r requirements.txt

# App
ADD pskspotter.py /app/


ENTRYPOINT [ "/entrypoint.sh" ]
