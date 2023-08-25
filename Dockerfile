FROM docker.io/library/python:3.11-alpine
RUN pip install --upgrade pip

WORKDIR /app

# Entry point
ADD entrypoint.sh /
RUN chmod +x /entrypoint.sh

# App
ADD pskspotter.py requirements.txt /app/
RUN wget https://www.country-files.com/cty/cty.plist
RUN pip install -r requirements.txt

ENTRYPOINT [ "/entrypoint.sh" ]
