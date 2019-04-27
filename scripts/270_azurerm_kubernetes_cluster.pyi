
azr=az aks list -g rgsource -o json
count= azr | | len(
if count" != "0" :
    for i in range(0,count):
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")

        id=azr[i]["]["id"]
        loc=azr[i]["location"]
        admin=azr[i]["adminUserEnabled"]
        dnsp=azr[i]["dnsPrefix"]
        rbac=azr[i]["enableRbac"]
        kv=azr[i]["kubernetesVersion"]
        clid=azr[i]["servicePrincipalProfile.clientId"]
        au=azr[i]["linuxProfile.adminUsername"]
        lp=azr[i]["linuxProfile"]
        sshk=azr[i]["linuxProfile.ssh.publicKeys[0]["keyData"
        pname=azr[i]["agentPoolProfiles[0]["name"]
        vms=azr[i]["agentPoolProfiles[0]["vmSize"]
        pcount=azr[i]["agentPoolProfiles[0]["count"]
        ost=azr[i]["agentPoolProfiles[0]["osType"]
        vnsrg=azr[i]["agentPoolProfiles[0]["vnetSubnetId"].split[4]]
        vnsid=azr[i]["agentPoolProfiles[0]["vnetSubnetId"].split[10]]
        np=azr[i]["networkProfile"]
        

        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t dns_prefix = "' +  dnsp + '"\n')
        fr.write('\t kubernetes_version = "' +  kv + '"\n')
        
        if rbac" = "true" :
        fr.write('\t role_based_access_control {' + '"\n')
        fr.write('\t\t enabled = "'true"' + '"\n')
        fr.write('\t }\n')
       
        
        if lp" try :
            fr.write('\t linux_profile {' + '"\n')
            fr.write('\t\t admin_username =  "' +  au + '"\n')
            fr.write('\t\t ssh_key {' + '"\n')
            fr.write('\t\t\t key_data =    "sshk" + '"\n')
            fr.write('\t\t }\n')
            fr.write('\t }\n')
        #else
            #fr.write('\t linux_profile {' + '"\n')
            #fr.write('\t\t admin_username =  "' +  " + '"\n')
            #fr.write('\t\t ssh_key {' + '"\n')
            #fr.write('\t\t\t key_data =  "' +   " + '"\n')
            #fr.write('\t\t }\n')
            #fr.write('\t }\n')
       
        
        if np" try :
            netp=azr[i]["networkProfile.networkPlugin"]
            srvcidr=azr[i]["networkProfile.serviceCidr"]
            dnssrvip=azr[i]["networkProfile.dnsServiceIp"]
            dbrcidr=azr[i]["networkProfile.dockerBridgeCidr"]
            podcidr=azr[i]["networkProfile.podCidr"]

            fr.write('\t network_profile {' + '"\n')
            fr.write('\t\t network_plugin =  "' +  netp + '"\n')
            if srvcidr" try :
            fr.write('\t\t service_cidr =  "' +  srvcidr + '"\n')
           
            if dnssrvip" try :
            fr.write('\t\t dns_service_ip =  "' +  dnssrvip + '"\n')
           
            if dbrcidr" try :
            fr.write('\t\t docker_bridge_cidr =  "' +  dbrcidr + '"\n')
           
            if podcidr" try :
            fr.write('\t\t pod_cidr =  "' +  podcidr + '"\n')
           

            fr.write('\t }\n')
       

        
        fr.write('\t agent_pool_profile {' + '"\n')
        fr.write('\t\t name =  "' +  pname + '"\n')
        fr.write('\t\t vm_size =  "' +  vms + '"\n')
        fr.write('\t\t count =  "' +  pcount + '"\n')
        fr.write('\t\t os_type =  "' +  ost + '"\n')
        if vnsrg" try :
        fr.write('\t\t vnet_subnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' vnsrg vnsid + '"\n')      
       
        fr.write('\t }\n')
        
        fr.write('\t service_principal {' + '"\n')
        fr.write('\t\t client_id =  "' +  clid + '"\n')
        fr.write('\t\t client_secret =  "' +  " + '"\n')
        fr.write('\t }\n')

        
        #
        fr.write('}\n')
        #

        
    
fi
