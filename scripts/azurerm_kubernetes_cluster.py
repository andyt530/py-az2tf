# azurerm_kubernetes_cluster
def azurerm_kubernetes_cluster(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_kubernetes_cluster"
    tcode="270-"
    azr=""
    if crf in tfp:
    # REST or cli
        print "REST Managed Disk"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Compute/disks"
        params = {'api-version': '2017-03-30'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]
        if cde:
            print(json.dumps(azr, indent=4, separators=(',', ': ')))

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print tfp,
        count=len(azr)
        print count
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-")

            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rg + '"\n')

    ###############
    # specific code start
    ###############

            admin=azr[i]["adminUserEnabled"]
            dnsp=azr[i]["dnsPrefix"]
            rbac=azr[i]["enableRbac"]
            kv=azr[i]["kubernetesVersion"]
            clid=azr[i]["servicePrincipalProfile"]["clientId"]
            au=azr[i]["linuxProfile"]["adminUsername"]
            lp=azr[i]["linuxProfile"]
            sshk=azr[i]["linuxProfile"]["ssh"]["publicKeys"][0]["keyData"]
            pname=azr[i]["agentPoolProfiles"][0]["name"]
            vms=azr[i]["agentPoolProfiles"][0]["vmSize"]
            pcount=azr[i]["agentPoolProfiles"][0]["count"]
            ost=azr[i]["agentPoolProfiles"][0]["osType"]
            vnsrg=azr[i]["agentPoolProfiles"][0]["vnetSubnetId"].split("/")[4]
            vnsid=azr[i]["agentPoolProfiles"][0]["vnetSubnetId"].split("/")[10]
            np=azr[i]["networkProfile"]
            

            fr.write('\t dns_prefix = "' +  dnsp + '"\n')
            fr.write('\t kubernetes_version = "' +  kv + '"\n')
            
            if rbac == "true" :
                fr.write('\t role_based_access_control { \n')
                fr.write('\t\t enabled = "true" \n')
                fr.write('\t }\n')
        
            
            try :
                lp=azr[i]["linuxProfile"]
                fr.write('\t linux_profile {' + '"\n')
                fr.write('\t\t admin_username =  "' +  au + '"\n')
                fr.write('\t\t ssh_key {' + '"\n')
                fr.write('\t\t\t key_data =    "' + sshk + '"\n')
                fr.write('\t\t }\n')
                fr.write('\t }\n')
            #else
                #fr.write('\t linux_profile {' + '"\n')
                #fr.write('\t\t admin_username =  "' +  " + '"\n')
                #fr.write('\t\t ssh_key {' + '"\n')
                #fr.write('\t\t\t key_data =  "' +   " + '"\n')
                #fr.write('\t\t }\n')
                #fr.write('\t }\n')
            except KeyError:
                pass
        
            
            try :
                np=azr[i]["networkProfile"]
                netp=azr[i]["networkProfile.networkPlugin"]
                srvcidr=azr[i]["networkProfile.serviceCidr"]
                dnssrvip=azr[i]["networkProfile.dnsService"]
                dbrcidr=azr[i]["networkProfile.dockerBridgeCidr"]
                podcidr=azr[i]["networkProfile.podCidr"]

                fr.write('\t network_profile {' + '"\n')
                fr.write('\t\t network_plugin =  "' +  netp + '"\n')
                try :
                    srvcidr=azr[i]["networkProfile.serviceCidr"]
                    fr.write('\t\t service_cidr =  "' +  srvcidr + '"\n')
                except KeyError:
                    pass
            
                try :
                    dnssrvip=azr[i]["networkProfile.dnsService"]
                    fr.write('\t\t dns_service_ip =  "' +  dnssrvip + '"\n')
                except KeyError:
                    pass
            
                try :
                    dbrcidr=azr[i]["networkProfile.dockerBridgeCidr"]
                    fr.write('\t\t docker_bridge_cidr =  "' +  dbrcidr + '"\n')
                except KeyError:
                    pass
            
                try :
                    podcidr=azr[i]["networkProfile.podCidr"]
                    fr.write('\t\t pod_cidr =  "' +  podcidr + '"\n')
                except KeyError:
                    pass

                fr.write('\t }\n')
            
            except KeyError:
                    pass

            fr.write('\t agent_pool_profile {' + '\n')
            fr.write('\t\t name =  "' + pname + '"\n')
            fr.write('\t\t vm_size =  "' + vms + '"\n')
            fr.write('\t\t count =  "' + pcount + '"\n')
            fr.write('\t\t os_type =  "' + ost + '"\n')

            try :
                vnsrg=azr[i]["agentPoolProfiles"][0]["vnetSubnetId"].split("/")[4]
                vnsid=azr[i]["agentPoolProfiles"][0]["vnetSubnetId"].split("/")[10]
                fr.write('\t\t vnet_subnet_id = "${azurerm_subnet.' + vnsrg + '__' + vnsid + '.id}" \n')      
            except KeyError:
                pass

            fr.write('\t }\n')
            
            fr.write('\t service_principal { \n')
            fr.write('\t\t client_id =  "' +  clid + '"\n')
            fr.write('\t\t client_secret =  ""\n')
            fr.write('\t }\n')


    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write('\t "' + key + '"="' + tval + '"\n')
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print f.read()

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
