FROM microsoft/azure-cli
RUN apk add --update python2 python2-dev 
RUN python2.7 -m ensurepip
RUN python2.7 -m pip install requests adal
ENV TF_VERSION="0.12.10"
RUN wget -qO- https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip | busybox unzip - ; chmod +x terraform ; mv terraform /bin/
ENV WORK_DIR="/tmp/aztf"
RUN mkdir -p ${WORK_DIR} && \
    git clone https://github.com/andyt530/py-az2tf.git ${WORK_DIR}
WORKDIR ${WORK_DIR}