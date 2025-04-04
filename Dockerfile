#Deriving the latest base image
FROM python:3.13.2-alpine3.21

# Add git
RUN apk add git

# Set the working directory
WORKDIR /usr/app/src

# Copy and install python modules required
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy needed files and set permissions accordingly
ADD https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64 /bin/dumb-init
COPY ./entrypoint.sh /root/entrypoint.sh
COPY ./run.sh /root/run.sh
RUN chmod 777 /root/entrypoint.sh /root/run.sh /bin/dumb-init

# Copy python script
COPY main.py .

# define dumb-init as the entrypoint
ENTRYPOINT ["dumb-init", "--"]

# set the command to execute
CMD /root/entrypoint.sh | while IFS= read -r line; do printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$line"; done;