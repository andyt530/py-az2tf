FROM microsoft/azure-cli 
ENV TERRAFORM_VERSION=0.11.11
VOLUME ["/az2tf"]
WORKDIR /az2tf
RUN mkdir /az2tf/scripts
RUN mkdir /az2tf/generated
RUN mkdir /az2tf/stub
RUN mkdir /az2tf/temp
RUN apk update && \
    wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/bin  
RUN apk add --no-cache ncurses
RUN apk add --no-cache bash
COPY az2tf.sh /az2tf
COPY scripts/*.sh /az2tf/scripts/
COPY stub/*.tf /az2tf/stub/
