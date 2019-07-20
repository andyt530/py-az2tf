FROM microsoft/azure-cli
RUN apk add --update python2 python2-dev
RUN python2.7 -m ensurepip
RUN python2.7 -m pip install requests adal
RUN wget -qO- https://releases.hashicorp.com/terraform/0.12.4/terraform_0.12.4_linux_amd64.zip | busybox unzip - ; chmod +x terraform ; mv terraform /usr/bin
