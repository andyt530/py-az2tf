
azr=az aks list -g rgsource -o json
count=print azr | jq '. | length'
if count" != "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
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
        vnsrg=azr[i]["agentPoolProfiles[0]["vnetSubnetId" | cut -d'/' -f5]
        vnsid=azr[i]["agentPoolProfiles[0]["vnetSubnetId" | cut -d'/' -f11]
        np=azr[i]["networkProfile"]
        
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile

        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t dns_prefix = "' +  dnsp + '"\n')
        fr.write('\t kubernetes_version = "' +  kv + '"\n')
        
        if rbac" = "true" :
        fr.write('\t role_based_access_control {' + '"\n')
        fr.write('\t\t enabled = "'true"' + '"\n')
        fr.write('\t }' + '"\n')
        fi
        
        if lp" != "null" :
            fr.write('\t linux_profile {' + '"\n')
            fr.write('\t\t admin_username =  "' +  au + '"\n')
            fr.write('\t\t ssh_key {' + '"\n')
            fr.write('\t\t\t key_data =    "sshk" + '"\n')
            fr.write('\t\t }' + '"\n')
            fr.write('\t }' + '"\n')
        #else
            #fr.write('\t linux_profile {' + '"\n')
            #fr.write('\t\t admin_username =  "' +  " + '"\n')
            #fr.write('\t\t ssh_key {' + '"\n')
            #fr.write('\t\t\t key_data =  "' +   " + '"\n')
            #fr.write('\t\t }' + '"\n')
            #fr.write('\t }' + '"\n')
        fi
        
        if np" != "null" :
            netp=azr[i]["networkProfile.networkPlugin"]
            srvcidr=azr[i]["networkProfile.serviceCidr"]
            dnssrvip=azr[i]["networkProfile.dnsServiceIp"]
            dbrcidr=azr[i]["networkProfile.dockerBridgeCidr"]
            podcidr=azr[i]["networkProfile.podCidr"]

            fr.write('\t network_profile {' + '"\n')
            fr.write('\t\t network_plugin =  "' +  netp + '"\n')
            if srvcidr" != "null" :
            fr.write('\t\t service_cidr =  "' +  srvcidr + '"\n')
            fi
            if dnssrvip" != "null" :
            fr.write('\t\t dns_service_ip =  "' +  dnssrvip + '"\n')
            fi
            if dbrcidr" != "null" :
            fr.write('\t\t docker_bridge_cidr =  "' +  dbrcidr + '"\n')
            fi
            if podcidr" != "null" :
            fr.write('\t\t pod_cidr =  "' +  podcidr + '"\n')
            fi

            fr.write('\t }' + '"\n')
        fi

        
        fr.write('\t agent_pool_profile {' + '"\n')
        fr.write('\t\t name =  "' +  pname + '"\n')
        fr.write('\t\t vm_size =  "' +  vms + '"\n')
        fr.write('\t\t count =  "' +  pcount + '"\n')
        fr.write('\t\t os_type =  "' +  ost + '"\n')
        if vnsrg" != "null" :
        fr.write('\t\t vnet_subnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' vnsrg vnsid + '"\n')      
        fi
        fr.write('\t }' + '"\n')
        
        fr.write('\t service_principal {' + '"\n')
        fr.write('\t\t client_id =  "' +  clid + '"\n')
        fr.write('\t\t client_secret =  "' +  " + '"\n')
        fr.write('\t }' + '"\n')

        
        #
        fr.write('}' + '"\n')
        #

        
    
fi
