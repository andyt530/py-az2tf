# RUNBOOK ON
import subprocess
import requests
import adal
import os
import json
import sys
import glob
import argparse
import ast
# RUNBOOK ON
 
#
# runbook auth
#
import automationassets

def get_automation_runas_token():
    """ Returs a token that can be used to authenticate against Azure resources """
    from OpenSSL import crypto
    import adal
   

    # Get the Azure Automation RunAs service principal certificate
    cert = automationassets.get_automation_certificate("AzureRunAsCertificate")
    sp_cert = crypto.load_pkcs12(cert)
    pem_pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, sp_cert.get_privatekey())

    # Get run as connection information for the Azure Automation service principal
    runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
    application_id = runas_connection["ApplicationId"]
    thumbprint = runas_connection["CertificateThumbprint"]
    tenant_id = runas_connection["TenantId"]

    # Authenticate with service principal certificate
    resource = "https://management.core.windows.net/"
    authority_url = ("https://login.microsoftonline.com/" + tenant_id)
    context = adal.AuthenticationContext(authority_url)
    azure_credential = context.acquire_token_with_client_certificate(
        resource,
        application_id,
        pem_pkey,
        thumbprint)
    
    # Return the token
    return azure_credential.get('accessToken') 
 
#
# azurerm_resource_group
#
import sys
def azurerm_resource_group(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    # handle resource groups
    isrun=False
    tfp="azurerm_resource_group"
    if crf in tfp:
        
        print('# ' + tfp,)
  
        tfrmf="001-"+tfp+"-staterm.sh"
        tfimf="001-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups"
        params = {'api-version': '2014-04-01'}
        r = requests.get(url, headers=headers, params=params)
        rgs= r.json()["value"]

        #frgfilename=tfp+".json"
        #frg=open(frgfilename, 'w')
        #frg.write(json.dumps(rgs, indent=4, separators=(',', ': ')))
        #frg.close()
        if cde:
            print(json.dumps(rgs, indent=4, separators=(',', ': ')))



        count=len(rgs)
        print (count)
        for j in range(0, count):
            
            name=rgs[j]["name"]
            rg=name
            loc=rgs[j]["location"]
            id=rgs[j]["id"]
            if crg is not None:
                if name.lower() != crg.lower():
                    continue
            
            rname=name.replace(".","-")
            if rg[0].isdigit(): rg="rg_"+rg
                
            if rname[0].isdigit(): rname="rg_"+rname
            prefix=tfp+"."+rname
            
            rfilename=prefix+".tf"
            if isrun:
                fr=sys.stdout
            else:
                fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource "' + tfp + '" "' + rname + '" {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
        

        # tags block
            try:
                mtags=rgs[j]["tags"]
            except:
                mtags="{}"
            tcount=len(mtags)-1
            if tcount > 1 :
                fr.write('tags = { \n')
                #print tcount
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
                fr.write('}\n')
            
            fr.write('}\n') 
            if fr is not sys.stdout: fr.close()  # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rname + '\n')
            tfim.write('echo "importing ' + str(j) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rname+' '+id+'\n'
            tfim.write(tfcomm)

        # end for
        tfrm.close()
        tfim.close()
        #end resource group 
#
# azurerm_management_lock
#
import uuid
def azurerm_management_lock(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    # management locks
    
    tfp="azurerm_management_lock"
    azr=""
    if crf in tfp:
        # REST
        # # print "REST VNets"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Authorization/locks"
        params = {'api-version': '2017-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="002-"+tfp+"-staterm.sh"
        tfimf="002-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for j in range(0, count):
            
            name=azr[j]["name"]
            print("name=",name)
            #name=name.encode('utf-8', 'ignore')
            print("name=",name)
            #loc=azr[j]["location"]
            id=azr[j]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
           
            level=azr[j]["properties"]["level"]
         
            scope1=id.split("/Microsoft.Authorization")[0].rstrip("providers")
            
            scope=scope1.rstrip("/")
            sc=len(scope.split("/"))
            #print sc
            sn=scope.split("/")[sc-1].replace(" ","-").lower()
            sn=sn.replace(".","-")

            #scope=scope.encode('utf-8', 'ignore')
            #sn=sn.encode('utf-8', 'ignore')
            
         

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[j], indent=4, separators=(',', ': ')))

            rname=name.replace(".","-")
            rname=rname.replace("[","-")
            rname=rname.replace("]","-")
            rname=rname.replace(" ","_")
            #try:
            #    rname=rname.encode('utf-8', 'ignore')
            #except UnicodeDecodeError:
            #    print('Problem with the name of this item: '+name)
            #    print('Please rename this item in the Azure Portal')
            #    rname=str(uuid.uuid4())
            #    #rname=rname.encode('utf-8', 'ignore')
                
                 
            try:
                prefix=tfp+"."+rg+'__'+rname+'__'+sn
            except UnicodeDecodeError:
                print('Problem with the scope name: '+scope)
                print('Please rename this item in the Azure Portal')
                sn=str(uuid.uuid4())
                #sn=sn.encode('utf-8', 'ignore')
                prefix=tfp+"."+rg+'__'+rname+'__'+sn
            #prefix=tfp+"."+rg+'__'+rname


            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write('resource ' + tfp + ' "' + rg + '__' + rname + '__'+ sn +  '" {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t lock_level = "'+ level + '"\n')   
            
            try:
                notes=azr[j]["properties"]["notes"]      
                #notes=notes.encode('utf-8', 'ignore')          
                fr.write('\t notes = "'+ notes + '"\n') 
            except KeyError:
                pass
            fr.write('\t scope = "'+ scope + '"\n')
        # tags block

    # tags block       
            try:
                mtags=azr[j]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    #fr.write(('\t "' + key + '"="' + tval + '"\n'))
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            #try:
            #    mtags=azr[j]["tags"]
            #except:
            #    mtags="{}"
            #tcount=len(mtags)-1
            #if tcount > 1 :
            #    fr.write('tags = { \n')
            #    print tcount
            #    for key in mtags.keys():
            #        tval=mtags[key]
            #        fr.write(('\t "' + key + '"="' + tval + '"\n'))
            #    #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
            #    fr.write('}\n')
            
            fr.write('}\n') 
            fr.close()  # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '__' + sn + '\n')
            
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname + '__'+ sn + ' "'+id+'"\n'
            tfim.write('echo "importing ' + str(j) + ' of ' + str(count-1) + '"' + '\n')
            #tfcomm=tfcomm.encode('utf-8', 'ignore')
            tfim.write(tfcomm)  

        # end for
        tfrm.close()
        tfim.close()
        #end management locks 
#
# azurerm_user_assigned_identity
#
def azurerm_user_assigned_identity(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    # 015 user assigned identity
    tfp="azurerm_user_assigned_identity"
    azr=""
    if crf in tfp:
        
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.ManagedIdentity/userAssignedIdentities"
        params = {'api-version': '2018-11-30'}
        r = requests.get(url, headers=headers, params=params)
        azr=r.json()["value"]


 
        tfrmf="015-"+tfp+"-staterm.sh"
        tfimf="015-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for j in range(0, count):
            
            name=azr[j]["name"]
            loc=azr[j]["location"]
            id=azr[j]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                print ("rgname=" + rg + " crg=" + crg)
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde: print(json.dumps(azr[j], indent=4, separators=(',', ': ')))
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "' + rgs + '"\n')
        # tags block
            try:
                mtags=azr[j]["tags"]
            except:
                mtags="{}"
            tcount=len(mtags)-1
            if tcount > 1 :
                fr.write('tags = { \n')
                #print tcount
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
                fr.write('}\n')
            
            fr.write('}\n') 
            fr.close()  # close .tf file

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
            
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write('echo "importing ' + str(j) + ' of ' + str(count-1) + '"' + '\n')
            tfim.write(tfcomm)  

        # end for
        tfrm.close()
        tfim.close()
        #end user assigned identity 
#
# azurerm_availability_set
#
def azurerm_availability_set(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  020 Avail Sets
    tfp="azurerm_availability_set"
    azr=""
    if crf in tfp:

        # print "REST Avail Set"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/availabilitySets"
        params = {'api-version': '2018-10-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="020-"+tfp+"-staterm.sh"
        tfimf="020-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
        
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            fd=str(azr[i]["properties"]["platformFaultDomainCount"])
            ud=str(azr[i]["properties"]["platformUpdateDomainCount"])
            #avm=azr[i]["virtualMachines"]
            skuname=azr[i]["sku"]["name"]
            rmtype="false"
            if "Aligned" in skuname:
                #print "skuname is true"
                rmtype="true"

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rgl=rg.lower()
            rname=name.replace(".","-").lower()
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')   
            fr.write('\t platform_fault_domain_count = "' + fd + '"\n')
            fr.write('\t platform_update_domain_count = "' + ud + '"\n')
            fr.write('\t managed = "' + rmtype + '"\n')

        # tags block
            
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                    #print tval
                #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
                fr.write('}\n')
            except KeyError:
                pass
            
            fr.write('}\n') 
            fr.close()   # close .tf file

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
                
            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end Avail Set 
#
# azurerm_route_table
#
def azurerm_route_table(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  030 Route Table
    tfp="azurerm_route_table"
    azr=""
    # debug - uncomment this line
    # cde=False
    if crf in tfp:
        # REST
        # print "REST ASG"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/routeTables"
        params = {'api-version': '2018-07-01'}
        r=requests.get(url, headers=headers, params=params)
        azr=r.json()["value"]



    #############
        tfrmf="030-"+tfp+"-staterm.sh"
        tfimf="030-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):
            try:
                name=azr[i]["name"]
                loc=azr[i]["location"]
                id=azr[i]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if rg[0].isdigit(): rg="rg_"+rg
                rgs=id.split("/")[4]   
            except KeyError:
                continue

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for

            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')   

        #
            # Interate routes
            #
            routes=azr[i]["properties"]["routes"]
            rcount=len(routes)
            for j in range(0, rcount):
                rtname=routes[j]["name"]
                adpr=routes[j]["properties"]["addressPrefix"]
                nhtype=routes[j]["properties"]["nextHopType"]

                fr.write('\t route {' + '\n')
                fr.write('\t\t name = "' + rtname + '"\n')
                fr.write('\t\t address_prefix = "' + adpr + '"\n')
                fr.write('\t\t next_hop_type = "' + nhtype + '"\n')
                try:
                    nhaddr=routes[j]["properties"]["nextHopIpAddress"]
                    fr.write('\t\t next_hop_in_ip_address = "' +  nhaddr + '"\n')
                except KeyError:
                    pass             
                fr.write('\t }' + '\n')

        # tags block
            
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                    #print tval
                #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
                fr.write('}\n')
            except KeyError:
                pass
            
            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())         

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
                
            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end route table 
#
# azurerm_application_security_group
#
def azurerm_application_security_group(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  040 ASG's
    tfp="azurerm_application_security_group"
    azr=""
    if crf in tfp:
        # REST
        # print "REST ASG"

        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/applicationSecurityGroups"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="040-"+tfp+"-staterm.sh"
        tfimf="040-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
        #    rg=azr[i]["resourceGroup"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            #print rg

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')   
            

        # tags block
            
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                    #print tval
                #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
                fr.write('}\n')
            except KeyError:
                pass
            
            fr.write('}\n') 
            fr.close()   # close .tf file

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
                
            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end ASG 
#
# azurerm_network_security_group
#
import ast
def azurerm_network_security_group(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  050 NSG's
    tfp="azurerm_network_security_group"
    azr=""
    if crf in tfp:
        # REST
        # print "REST NSG"

        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/networkSecurityGroups"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="050-"+tfp+"-staterm.sh"
        tfimf="050-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rgs=id.split("/")[4]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')   
            #
            # Security Rules
            #
            #try:
            srules=azr[i]["properties"]["securityRules"]
            #print srules
            scount=len(srules)
            for j in range(0, scount):  
                #print "j=" + str(j)            
                fr.write('\t security_rule {\n')
                srname=srules[j]["name"]  
                #print "Security Rule " + srname                   
                fr.write('\t\t name = "' +  srname + '"\n')
                try:
                    srdesc=srules[j]["properties"]["description"]                    
                    fr.write('\t\t description = "' + srdesc + '"\n')
                except KeyError:
                    pass

                sraccess=srules[j]["properties"]["access"]                       
                fr.write('\t\t access = "' +  sraccess + '"\n')
                srpri=str(srules[j]["properties"]["priority"])
                fr.write('\t\t priority = "' + srpri + '"\n')
                srproto=srules[j]["properties"]["protocol"]
                fr.write('\t\t protocol = "' + srproto + '"\n')
                srdir=srules[j]["properties"]["direction"] 
                fr.write('\t\t direction = "' +  srdir + '"\n')
        #source address block
                try:
                    srsp=str(srules[j]["properties"]["sourcePortRange"])
                    fr.write('\t\t source_port_range = "' + srsp + '"\n')
                except KeyError:
                    pass
                    
                srsps=str(ast.literal_eval(json.dumps(srules[j]["properties"]["sourcePortRanges"])))
                srsps=srsps.replace("'",'"')
                if srsps != "[]" :
                    fr.write('\t\t source_port_ranges = ' + srsps + '\n')
                    
                try:
                    srsap=srules[j]["properties"]["sourceAddressPrefix"] 
                    fr.write('\t\t source_address_prefix = "'+ srsap + '"\n')
                except KeyError:
                    pass
                    
                srsaps=str(ast.literal_eval(json.dumps(srules[j]["properties"]["sourceAddressPrefixes"])))
                srsaps=srsaps.replace("'",'"')

                if srsaps != "[]" :
                    fr.write('\t\t source_address_prefixes = ' + srsaps + '\n')

    #destination address block
                try:
                    srdp=str(srules[j]["properties"]["destinationPortRange"]) 
                    fr.write('\t\t destination_port_range = "' + srdp + '"\n')
                except KeyError:
                    pass
                
                srdps=str(ast.literal_eval(json.dumps(srules[j]["properties"]["destinationPortRanges"])))
                srdps=srdps.replace("'",'"')
                if srdps != "[]" :
                    fr.write('\t\t destination_port_ranges = ' + srdps + '\n')

                try:
                    srdap=srules[j]["properties"]["destinationAddressPrefix"]
                    fr.write('\t\t destination_address_prefix = "'+ srdap + '"\n')
                except KeyError:
                    pass
                
                srdaps=str(ast.literal_eval(json.dumps(srules[j]["properties"]["destinationAddressPrefixes"])))
                srdaps=srdaps.replace("'",'"')
                if srdaps != "[]" :
                    fr.write('\t\t destination_address_prefixes = ' + srdaps + '\n')

        # source asg's
                try:
                    srsasgs=srules[j]["properties"]["sourceApplicationSecurityGroups"]
                    kcount=len(srsasgs)
                except KeyError:
                    kcount=0

                for k in range(0, kcount):
                    #print "in k k=" + str(k)
                    asgnam=srules[j]["properties"]["sourceApplicationSecurityGroups"][k]["id"].split("/")[8].replace(".","-")
                    asgrg=srules[j]["properties"]["sourceApplicationSecurityGroups"][k]["id"].split("/")[4].replace(".","-").lower()   
                    if asgrg[0].isdigit(): asgrg="rg_"+asgrg
                    fr.write('\t\t source_application_security_group_ids = ["${azurerm_application_security_group.' + asgrg + '__' + asgnam + '.id}"]' + '\n')
                        
        # destination asg's
                try:
                    srdasgs=srules[j]["properties"]["destinationApplicationSecurityGroups"]
                    kcount=len(srdasgs)
                except KeyError:
                    kcount=0
                for k in range(0, kcount):
                    asgnam=srules[j]["properties"]["destinationApplicationSecurityGroups"][k]["id"].split("/")[8].replace(".","-")
                    asgrg=srules[j]["properties"]["destinationApplicationSecurityGroups"][k]["id"].split("/")[4].replace(".","-").lower()  
                    if asgrg[0].isdigit(): asgrg="rg_"+asgrg
                    fr.write('\t\t destination_application_security_group_ids = ["${azurerm_application_security_group.' + asgrg + '__' + asgnam + '.id}"]' + '\n')
                        
                fr.write('\t}' + '\n')
                
                # end for j loop   
            #except KeyError:
            #    print "No security rules"

        # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    #fr.write(('\t "' + key + '"="' + tval + '"\n'))
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                    #print tval
                #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
                fr.write('}\n')
            except KeyError:
                pass
            
            fr.write('}\n') 
            fr.close()   # close .tf file
            
            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
        #end NSG 
#
# azurerm_virtual_network
#
import ast
def azurerm_virtual_network(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  060 Virtual Networks
    tfp="azurerm_virtual_network"
    azr=""
    if crf in tfp:
        # REST
        # print "REST VNets"

        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/virtualNetworks"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="060-"+tfp+"-staterm.sh"
        tfimf="060-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')
            
            addsp=azr[i]["properties"]["addressSpace"]["addressPrefixes"]
            laddsp='['
            for x in addsp:
                laddsp=laddsp+'"'+x+'",'
            laddsp=laddsp+']'
            #print laddsp
            fr.write('\taddress_space =  ' + laddsp + '\n')
            try:
                dns=str(ast.literal_eval(json.dumps(azr[i]["properties"]["dhcpOptions"]["dnsServers"])))
                dns=dns.replace("'",'"')
                if "[]" not in dns:
                    fr.write('\t dns_servers =  ' + dns + '\n')
            except KeyError:
                pass        


            #
            #loop around subnets
            #
            subs=azr[i]["properties"]["subnets"]
            jcount=len(subs)
            for j in range(0,jcount):
                snname=subs[j]["name"]
                snaddr=subs[j]["properties"]["addressPrefix"]

                fr.write('\tsubnet {\n')
                fr.write('\t\t name = "'+ snname + '"\n')
                fr.write('\t\t address_prefix = "' + snaddr + '"\n')
                try:
                    snnsgid=subs[j]["properties"]["networkSecurityGroup"]["id"]
                    nsgnam=snnsgid.split("/")[8].replace(".","-")
                    nsgrg=snnsgid.split("/")[4].replace(".","-").lower() 
                    if nsgrg[0].isdigit(): nsgrg="rg_"+nsgrg        
                    fr.write('\t\t security_group = "${azurerm_network_security_group.' + nsgrg + '__' + nsgnam + '.id}"' + '\n')
                except KeyError: 
                    pass
                
                fr.write('\t}' + '\n')

        # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
        return azr
    #end VNET
    ############# 
#
# azurerm_subnet
#
import ast
def azurerm_subnet(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  070 subnets
    tfp="azurerm_subnet"
    azr=""
    if crf in tfp:
        # REST
        # print "REST VNets"

        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/virtualNetworks"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

    # subnet in vnet
        tfrmf="070-"+tfp+"-staterm.sh"
        tfimf="070-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):
            subs=azr[i]["properties"]["subnets"]
            vnetname=azr[i]["name"]
            jcount=len(subs)
            

            for j in range(0, jcount):
                name=subs[j]["name"]
                #loc=subs[j]["location"] subnets don't have location
                id=subs[j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if rg[0].isdigit(): rg="rg_"+rg
                rgs=id.split("/")[4]
                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for
                if cde:
                    print(json.dumps(subs[j], indent=4, separators=(',', ': ')))
                
                rname=name.replace(".","-")
                prefix=tfp+"."+rg+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t virtual_network_name = "' + vnetname + '"\n') 
                fr.write('\t resource_group_name = "' +  rgs + '"\n')

                sprefix=subs[j]["properties"]["addressPrefix"]
                fr.write('\t address_prefix = "' +  sprefix + '"\n')
                rtbid="null"
                try:
                    seps=subs[j]["properties"]["serviceEndpoints"]
                    kcount=len(seps)
                    #print (json.dumps(seps, indent=4, separators=(',', ': ')))
                    #print kcount
                    lseps='['
                    for k in range(0, kcount):
                        x=seps[k]["service"]
                        lseps=lseps+'"'+x+'",'
                    lseps=lseps+']'
                    fr.write('\t service_endpoints = '+ lseps + '\n')
                except KeyError:
                    pass
                
                try:
                    snsgid=subs[j]["properties"]["networkSecurityGroup"]["id"].split("/")[8].replace(".","-")
                    snsgrg=subs[j]["properties"]["networkSecurityGroup"]["id"].split("/")[4].replace(".","-").lower()
                    if snsgrg[0].isdigit(): snsgrg="rg_"+snsgrg
                    fr.write('\t network_security_group_id = "${azurerm_network_security_group.' + snsgrg + '__' + snsgid +'.id}"' + '\n')
                except KeyError:
                    pass
                
                try:
                    rtbid=subs[j]["properties"]["routeTable"]["id"].split("/")[8].replace(".","-")
                    rtrg=subs[j]["properties"]["routeTable"]["id"].split("/")[4].replace(".","-").lower()
                    if rtrg[0].isdigit(): rtrg="rg_"+rtrg
                    fr.write('\t route_table_id = "${azurerm_route_table.' + rtrg + '__' + rtbid +'.id}"' + '\n')
                except KeyError:
                    pass   

                try:
                    delegn=subs[j]["properties"]["delegations"]
                    kcount=len(delegn)
                    for k in range(0, kcount):
                        delegn=subs[j]["properties"]["delegations"][k]["name"]
                        fr.write('delegation {\n')
                        fr.write('\t name = "' + delegn + '"\n')
                        try:
                            sdn=subs[j]["properties"]["delegations"][k]["properties"]["serviceName"]
                            sdact=str(ast.literal_eval(json.dumps(subs[j]["properties"]["delegations"][k]["properties"]["actions"])))                                 
                            sdact=sdact.replace("'",'"')
                            fr.write('\t service_delegation {\n')
                            fr.write('\t name = "' + sdn + '"\n')
                            #fr.write('\t actions = ' + sdact + '\n')
                            fr.write('\t} \n')
                        except KeyError:
                            pass         

                        fr.write('} \n')
                    # end k loop
                except KeyError:
                    pass 


                fr.write('}' + ' \n')

    # azurerm_subnet_network_security_group_association
        
                r1="skip"
                try:
                    snsgid=subs[j]["properties"]["networkSecurityGroup"]["id"].split("/")[8].replace(".","-")
                    r1="azurerm_subnet_network_security_group_association"
                    fr.write('resource ' + r1 + ' ' + rg + '__' + rname + '__' + snsgid + ' {\n') 
                    fr.write('\tsubnet_id = "${azurerm_subnet.' + rg + '__' + rname + '.id}"' + '\n')
                    if snsgrg[0].isdigit(): snsgrg="rg_"+snsgrg
                    fr.write('\tnetwork_security_group_id = "${azurerm_network_security_group.' + snsgrg + '__' + snsgid +'.id}"' + '\n')
                    fr.write('}' + ' \n')
                except KeyError:
                    pass
                    

    # azurerm_subnet_route_table_association

                r2="skip"
                try:
                    rtbid=subs[j]["properties"]["routeTable"]["id"].split("/")[8].replace(".","-")
                    r2="azurerm_subnet_route_table_association"
                    fr.write('resource ' + r2 + ' ' + rg + '__' + rname + '__' + rtbid + ' {\n') 
                    fr.write('\tsubnet_id = "${azurerm_subnet.' + rg + '__' + rname + '.id}"' + '\n')
                    if rtrg[0].isdigit(): rtrg="rg_"+rtrg
                    fr.write('\troute_table_id = "${azurerm_route_table.' + rtrg + '__' + rtbid +'.id}"' + '\n')
                    fr.write('}' + ' \n')
                except KeyError:
                    pass
                

                #fr.write('}\n') 
                fr.close()   # close .tf file


                # azurerm_subnet

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(j) + ' of ' + str(jcount-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm) 

    # azurerm_subnet_network_security_group_association

                if "skip" not in r1:
        
                    tfrm.write('terraform state rm ' + r1 + '.' + rg + '__' + rname + '__' + snsgid + '\n')
                    tfcomm='terraform import '+r1 +'.'+rg+'__'+rname+'__'+snsgid+' '+id+'\n'
                    tfim.write(tfcomm)
            

    # azurerm_subnet_route_table_association

                if "skip" not in r2:

                    tfrm.write('terraform state rm ' + r2 + '.' + rg + '__' + rname + '__' + rtbid + '\n')
                    tfcomm='terraform import '+r2 +'.'+rg+'__'+rname+'__'+rtbid+' '+id+'\n'
                    tfim.write(tfcomm)
                

            # end j

        ###############
        # specific code end
        ###############
    

        # end for i loop

        tfrm.close()
        tfim.close()
    #end subnet 
#
# azurerm_virtual_network_peering
#
def azurerm_virtual_network_peering(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #############
    #  080 vnet peering
    tfp="azurerm_virtual_network_peering"
    if crf in tfp: 
    # peering in vnet

        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/virtualNetworks"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="080-"+tfp+"-staterm.sh"
        tfimf="080-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):
            peers=azr[i]["properties"]["virtualNetworkPeerings"]
            vnetname=azr[i]["name"]
            jcount=len(peers)
            
            for j in range(0, jcount):
                name=peers[j]["name"]
                #loc=peers[j]["location"] peers don't have a location
                id=peers[j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if rg[0].isdigit(): rg="rg_"+rg
                rgs=id.split("/")[4]

                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for
                if cde:
                    print(json.dumps(peers[j], indent=4, separators=(',', ': ')))
                    
                rname=name.replace(".","-")
                prefix=tfp+"."+rg+'__'+rname
                    
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write("")
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')
                fr.write('\t virtual_network_name = "' + vnetname + '"\n')


                rvnid=peers[j]["properties"]["remoteVirtualNetwork"]["id"]
                aft=str(peers[j]["properties"]["allowForwardedTraffic"]).lower()
                agt=str(peers[j]["properties"]["allowGatewayTransit"]).lower()
                avna=str(peers[j]["properties"]["allowVirtualNetworkAccess"]).lower()
                urg=str(peers[j]["properties"]["useRemoteGateways"]).lower()

                fr.write('\t remote_virtual_network_id = "' +  rvnid + '"\n')
                fr.write('\t allow_forwarded_traffic = ' +  aft + '\n')
                fr.write('\t allow_gateway_transit = ' +  agt + '\n')
                fr.write('\t allow_virtual_network_access = ' +  avna + '\n')
                fr.write('\t use_remote_gateways = ' +  urg + '\n')
                            
                fr.write('}\n') 
                fr.close()   # close .tf file

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(j) + ' of ' + str(jcount-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  
            # end for j loop
        # end for i loop

        tfrm.close()
        tfim.close()
    #end peering 
#
# azurerm_managed_disk
#
def azurerm_managed_disk(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_managed_disk"
    azr=""
    if crf in tfp:
    # REST or cli
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/disks"
        params = {'api-version': '2017-03-30'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="100-"+tfp+"-staterm.sh"
        tfimf="100-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            oname=azr[i]["name"]
            name=oname.replace("/.vhd","/_vhd") 
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')


            try:
                ostyp=azr[i]["properties"]["osType"]
                fr.write('\t os_type = "' +  ostyp + '"\n')
            except KeyError:
                pass
                
            try:
                creopt=azr[i]["properties"]["creationData"]["createOption"]
                fr.write('\t create_option = "' +  creopt + '"\n')
            except KeyError:
                pass

            try:
                creopt=azr[i]["properties"]["creationData"]["sourceResourceId"]
                fr.write('\t source_resource_id = "' +  creopt + '"\n')
            except KeyError:
                pass        

            try:
                imid=azr[i]["properties"]["creationData"]["imageReference"]["id"]
                fr.write('\t image_reference_id = "' +  imid + '"\n')
            except KeyError:
                pass 
            """        
            try:      
                creid=azr[i]["properties"]["creationData"]["imageReference"]["id"]
                fr.write('\t source_resource_id = "' +  creid + '"\n')
            except KeyError:
                pass
            """        
            try:
                enc=azr[i]["properties"]["encryptionSettings"]["enabled"]
                fr.write('\t encryption_settings { \n')
                fr.write('\t\t enabled = ' +  str(enc).lower() + '\n')
                try:
                    kekurl=azr[i]["properties"]["encryptionSettings"]["keyEncryptionKey"]["keyUrl"]
                    kekvltid=azr[i]["properties"]["encryptionSettings"]["keyEncryptionKey"]["sourceVault"]["id"]
                    fr.write('\t\t key_encryption_key { \n')
                    fr.write('\t\t\t key_url = "' +  kekurl + '"\n')
                    fr.write('\t\t\t source_vault_id = "' +  kekvltid + '"\n')
                    fr.write('\t\t } \n')
                except KeyError:
                    pass       

                try:
                    dekurl=azr[i]["properties"]["encryptionSettings"]["diskEncryptionKey"]["secretUrl"]
                    dekvltid=azr[i]["properties"]["encryptionSettings"]["diskEncryptionKey"]["sourceVault"]["id"]
                    fr.write('\t\t disk_encryption_key { \n')
                    fr.write('\t\t\t secret_url = "' +  dekurl + '"\n')
                    fr.write('\t\t\t source_vault_id = "' +  dekvltid + '"\n')               
                    fr.write('\t\t } \n')
                except KeyError:
                    pass


                fr.write('\t } \n')
            except KeyError:
                pass


            try:
                stopt=azr[i]["sku"]["name"]
                fr.write('\t storage_account_type = "' +  stopt + '"\n')
            except KeyError:
                fr.write('\t storage_account_type = "' +  "StandardSSD_LRS" + '"\n')
                pass    
            
        

            try:
                dsize=str(azr[i]["properties"]["diskSizeGB"])
                fr.write('\t disk_size_gb = "' +  dsize + '"\n')
                    
            except KeyError:
                pass


            try:
                zones=azr[i]["zones"]
                fr.write('zones = ')
                fr.write(json.dumps(zones, indent=4, separators=(',', ': ')))
                fr.write('\n')
            except KeyError:
                pass

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end managed disk 
#
# azurerm_storage_account
#
import ast
def azurerm_storage_account(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  110 storage account
    
    tfp="azurerm_storage_account"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Storage Acc"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Storage/storageAccounts"
        params = {'api-version': '2019-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="110-"+tfp+"-staterm.sh"
        tfimf="110-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ('# '+tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde: print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            satier=azr[i]["sku"]["tier"]
            sakind=azr[i]["kind"]
            
            sartype=azr[i]["sku"]["name"].split("_")[1]
            saencrypt=str(azr[i]["properties"]["encryption"]["services"]["blob"]["enabled"]).lower()
            fiencrypt=str(azr[i]["properties"]["encryption"]["services"]["file"]["enabled"]).lower()
            sahttps=str(azr[i]["properties"]["supportsHttpsTrafficOnly"]).lower()
            #nrs=azr[i]["properties"]["networkAcls"]
            saencs=azr[i]["properties"]["encryption"]["keySource"]
            
            fr.write('\t account_tier = "' + satier + '"\n')
            fr.write('\t account_kind = "' + sakind + '"\n')
            fr.write('\t account_replication_type = "' +  sartype + '"\n')
            fr.write('\t enable_blob_encryption = ' +  saencrypt + '\n')
            fr.write('\t enable_file_encryption = ' +  fiencrypt + '\n')
            fr.write('\t enable_https_traffic_only = ' +  sahttps + '\n')
            fr.write('\t account_encryption_source = "' +  saencs + '"\n')
            #fr.write('\t enable_advanced_threat_protection = ' +  'false' + '\n')

            try:
                ishns=str(azr[i]["properties"]["isHnsEnabled"]).lower()
                fr.write('\t is_hns_enabled = ' + ishns + '\n')
            except KeyError:
                pass   


            try:        
                byp=str(ast.literal_eval(json.dumps(azr[i]["properties"]["networkAcls"]["bypass"])))
                byp=byp.replace("'",'"')
                byp=byp.replace(", ",'", "')
                dfa=azr[i]["properties"]["networkAcls"]["defaultAction"]
                ipr=azr[i]["properties"]["networkAcls"]["ipRules"]
                #print(json.dumps(ipr, indent=4, separators=(',', ': ')))


                vnr=azr[i]["properties"]["networkAcls"]["virtualNetworkRules"]
                
                icount=len(ipr)
                vcount=len(vnr)
            
                # if off skip
                if "None" not in byp and "Allow" not in dfa :
                # if the only network rule is AzureServices, dont need a network_rules block
                    if "AzureServices" not in byp or icount > 0 or vcount > 0:
                        fr.write('\t network_rules { \n')
                        fr.write('\t\t default_action = "' +  dfa + '"\n')
                        fr.write('\t\t bypass = ["' +  byp + '"]\n')
                        
                        if icount > 0:
                            fr.write('\t\t ip_rules = [')
                            for ic in range(0, icount): 
                                ipa=ipr[ic]["value"]
                                fr.write('"' + ipa + '",')
                            fr.write(']\n')
                        if vcount > 0:
                            fr.write('\t\t virtual_network_subnet_ids = [')
                            for vc in range(0,vcount):
                                vnsid=vnr[vc]["id"]
                                fr.write('\t\t"' + vnsid + '",')
                            fr.write(']\n')
                        fr.write('}\n')
                    # end if
                # end if

            except KeyError:
                pass            

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end storage account 
#
# azurerm_key_vault
#
def azurerm_key_vault(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #############
    #  090 key vault
    
    tfp="azurerm_key_vault"
    azr=""
    if crf in tfp:
        # REST or cli

        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.KeyVault/vaults"
        params = {'api-version': '2016-10-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="090-"+tfp+"-staterm.sh"
        tfimf="090-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            sku=azr[i]["properties"]["sku"]["name"]
            if sku == "Premium" : sku="premium" 
            if sku == "Standard" : sku="standard" 
    
              
            fr.write('\t sku_name="' + sku + '"\n')
          

            ten=azr[i]["properties"]["tenantId"]     
            fr.write('\t tenant_id="' + ten + '"\n')


            try:
                #netacls=azr[i]["properties"]["networkAcls"]
                netacldf=azr[i]["properties"]["networkAcls"]["defaultAction"]
                netaclby=azr[i]["properties"]["networkAcls"]["bypass"]
                netaclipr=azr[i]["properties"]["networkAcls"]["ipRules"]
                vnr=azr[i]["properties"]["networkAcls"]["virtualNetworkRules"]
                vcount=len(vnr)
                ipcount=len(netaclipr)

                
                fr.write('\t network_acls {\n')
                fr.write('\t\t bypass="' + netaclby + '"\n')
                fr.write('\t\t default_action="' + netacldf + '"\n')
                
                if ipcount > 0 :
                    print(json.dumps(netaclipr, indent=4, separators=(',', ': ')))
                    fr.write('\t\t ip_rules = [\n')
                    for ip in range(0, ipcount): 
                        aip=netaclipr[ip]["value"]
                        fr.write('\t\t\t"'+aip + '",\n')
                    fr.write('\t\t ]' + '\n')
                
                
                if vcount > 0:
                    fr.write('\t\t virtual_network_subnet_ids = [\n')
                    for v in range(0, vcount): 
                        aid=vnr[v]["id"]
                        fr.write('\t\t\t"'+aid + '",\n')
                    fr.write('\t\t ]' + '\n')
                    
                fr.write('\t }' + '\n')
            except KeyError:
                pass


            try: 
                endep=str(azr[i]["properties"]["enabledForDeployment"]).lower()
                fr.write('\t enabled_for_deployment=' + endep + '\n')
            except KeyError:
                pass
            
            try:
                endisk=str(azr[i]["properties"]["enabledForDiskEncryption"]).lower()
                if endisk != "None":
                    fr.write('\t enabled_for_disk_encryption=' + endisk + '\n')
            except KeyError:
                pass       
            
            try:
                entemp=str(azr[i]["properties"]["enabledForTemplateDeployment"]).lower()
                if entemp != "None":
                    fr.write('\t enabled_for_template_deployment=' +  entemp + '\n')
            except KeyError:
                pass

            ap=azr[i]["properties"]["accessPolicies"]
                    
            #
            # Access Policies
            #
            pcount=len(ap)
            for j in range(0, pcount):    
                fr.write('\t access_policy {' + '\n')
                apten=azr[i]["properties"]["accessPolicies"][j]["tenantId"]           
                fr.write('\t\t tenant_id="' + apten + '"\n')
                apoid=azr[i]["properties"]["accessPolicies"][j]["objectId"]
                fr.write('\t\t object_id="' + apoid + '"\n')

                try:         
                    jkl=azr[i]["properties"]["accessPolicies"][j]["permissions"]["keys"]    
                    try:
                        kl=len(jkl)
                        fr.write('\t\t key_permissions = [ \n')
                        for k in range(0,kl):
                            tk=azr[i]["properties"]["accessPolicies"][j]["permissions"]["keys"][k]
                            if tk != "all":
                                fr.write('\t\t\t "' + tk + '",\n')
                        fr.write('\t\t ]\n') 
                    except TypeError:
                        pass 
                except KeyError:
                    pass

                try:
                    jsl=azr[i]["properties"]["accessPolicies"][j]["permissions"]["secrets"]
                    try:
                        sl=len(jsl)
                        fr.write('\t\t secret_permissions = [ \n')
                        for k in range(0,sl):
                            tk=azr[i]["properties"]["accessPolicies"][j]["permissions"]["secrets"][k]
                            if tk != "all":
                                fr.write('\t\t\t "' + tk + '",\n')
                        fr.write('\t\t ]\n') 
                    except TypeError:
                        pass 
                except KeyError:
                    pass
                
                try:
                    jcl=azr[i]["properties"]["accessPolicies"][j]["permissions"]["certificates"]
                    try:
                        cl=len(jcl)
                        fr.write('\t\t certificate_permissions = [ \n')
                        for k in range(0,cl):
                            tk=azr[i]["properties"]["accessPolicies"][j]["permissions"]["certificates"][k]
                            if tk != "all":    
                                fr.write('\t\t\t "' + tk + '",\n')
                        fr.write('\t\t ]\n')                          
                        
                    except TypeError:
                        pass       
                except KeyError:
                    pass
                fr.write('\t}\n')
            
    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            

            fr.write('} \n')
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end key vault 
#
# azurerm_public_ip
#
def azurerm_public_ip(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_public_ip"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/publicIPAddresses"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="120-"+tfp+"-staterm.sh"
        tfimf="120-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')
            try:
                sku=azr[i]["sku"]["name"]
                fr.write('\t sku = "' + sku + '"\n')
            except KeyError:
                pass
            #timo=azr[i]["properties"]["idleTimeoutInMinutes"]
            try:
                dnsname=azr[i]["properties"]["dnsSettings"]["domainNameLabel"]
                fr.write('\t domain_name_label = "' +  dnsname + '"\n')
            except KeyError:
                pass

            #try:
                #dnsfqdn=azr[i]["properties"]["dnsSettings"]["fqdn"]
            #except KeyError:
                #pass
            
            try:
                subipalloc=azr[i]["properties"]["publicAllocationMethod"]
                fr.write('\t allocation_method = "' +    subipalloc + '"\n')
            except KeyError:
                pass

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end public ip 
#
# azurerm_traffic_manager_profile
#
def azurerm_traffic_manager_profile(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  124 Traffic manager profile
    tfp="azurerm_traffic_manager_profile"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Traffic Manager Profile"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/trafficmanagerprofiles"
        params = {'api-version': '2017-05-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="124-"+tfp+"-staterm.sh"
        tfimf="124-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            #loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            #fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            trm=azr[i]["properties"]["trafficRoutingMethod"]
            fr.write('\t traffic_routing_method = "' +  trm + '"\n')
            ps=azr[i]["properties"]["profileStatus"]
            fr.write('\t profile_status = "' + ps + '"\n') 
        
            #dnsc=azr[i]["properties"]["dnsConfig"]
            #monc=azr[i]["properties"]["monitorConfig"]
                    

    # dns_config block

            rn=azr[i]["properties"]["dnsConfig"]["relativeName"]
            ttl=azr[i]["properties"]["dnsConfig"]["ttl"]
            
            if ttl == 0: 
                ttl=30
            
            fr.write('\t dns_config { \n')
            fr.write('\t\t relative_name = "' + rn + '"\n')
            #TF bug returning 0
            fr.write('\t\t ttl  = "' + str(ttl) + '"\n')
            fr.write('\t} \n')
            
    # monitor_config block

            prot=azr[i]["properties"]["monitorConfig"]["protocol"]
            port=azr[i]["properties"]["monitorConfig"]["port"]

            fr.write('\t monitor_config { \n')
            fr.write('\t\t protocol = "' + prot + '"\n')
            fr.write('\t\t port  = "' + str(port) + '"\n')
            try:
                path=azr[i]["properties"]["monitorConfig"]["path"]
                if path is not None:
                    fr.write('\t\t path  = "' + path + '"\n')
            except KeyError:
                pass
            fr.write('\t} \n')  
            


    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
        return azr
    #end traffic manager profile 
#
# azurerm_traffic_manager_endpoint
#
def azurerm_traffic_manager_endpoint(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  125 traffic manager endpoint

    tfp="azurerm_traffic_manager_endpoint"

    if crf in tfp:
    # REST or cli

        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/trafficmanagerprofiles"
        params = {'api-version': '2017-05-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="125-"+tfp+"-staterm.sh"
        tfimf="125-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            #loc=azr[i]["location"]
            id=azr[i]["id"]
            pname=azr[i]["name"]
            azr2=azr[i]["properties"]["endpoints"]
            jcount=len(azr2)
            
            for j in range (0,jcount):

                name=azr2[j]["name"]
                id=azr2[j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if rg[0].isdigit(): rg="rg_"+rg
                rgs=id.split("/")[4]
                
                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for
                if cde:
                    print(json.dumps(azr2[j], indent=4, separators=(',', ': ')))
                
                rname=name.replace(".","-")
                prefix=tfp+"."+rg+'__'+rname
                
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                #fr.write('\t location = "'+ loc + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')
                fr.write('\t profile_name = "' +  pname + '"\n')
                ttype=azr2[j]["type"].split("/")[2]
                fr.write('\t type = "' +  ttype + '"\n')
               
                pri=azr2[j]["properties"]["priority"]
                fr.write('\t priority = "' +  str(pri) + '"\n')
                wt=azr2[j]["properties"]["weight"]
                fr.write('\t weight = "' +  str(wt) + '"\n')

                tgt=azr2[j]["properties"]["target"]
                fr.write('\t target = "' +  tgt + '"\n')
                eps=azr2[j]["properties"]["endpointStatus"]
                fr.write('\t endpoint_status = "' +  eps + '"\n')
                try:
                    #tgtid=azr2[j]["properties"]["targetResourceId"]
                    tgtrrg=azr2[j]["properties"]["targetResourceId"].split("/")[4].replace(".","-").lower()
                    tgtrid=azr2[j]["properties"]["targetResourceId"].split("/")[8].replace(".","-")          
                    if tgtrrg[0].isdigit(): tgtrrg="rg_"+tgtrrg
                    fr.write('\t target_resource_id = "${azurerm_public_ip.' + tgtrrg + '__' + tgtrid + '.id}"\n')
                except KeyError:
                    pass


                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  
            # end for j loop

        # end for i loop

        tfrm.close()
        tfim.close()
    #end traffic manager endpoint 
#
# azurerm_network_interface
#
def azurerm_network_interface(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    
    tfp="azurerm_network_interface"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/networkInterfaces"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="130-"+tfp+"-staterm.sh"
        tfimf="130-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rgs=id.split("/")[4]
            rg=id.split("/")[4].replace(".","-").lower()
            
            if rg[0].isdigit(): rg="rg_"+rg
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            ipfor=azr[i]["properties"]["enableIPForwarding"]
            netacc=azr[i]["properties"]["enableAcceleratedNetworking"]
            ipcon=azr[i]["properties"]["ipConfigurations"]
          
            #fr.write('\t internal_dns_name_label  = "' +  ipfor + '"\n')
            fr.write('\t enable_ip_forwarding = ' +  str(ipfor).lower() + '\n')
            fr.write('\t enable_accelerated_networking  = ' +  str(netacc).lower() + '\n')
            #fr.write('\t dns_servers  = "' +  ipfor + '"\n')
            #privip0=azr[i]["properties"]["ipConfigurations"][0]["privateIPAddress"]

            try:
                snsg=azr[i]["properties"]["networkSecurityGroup"]["id"].split("/")[8].replace(".","-")
                snsgrg=azr[i]["properties"]["networkSecurityGroup"]["id"].split("/")[4].replace(".","-").lower()
                if snsgrg[0].isdigit(): snsgrg="rg_"+snsgrg
                fr.write('\t network_security_group_id = "${azurerm_network_security_group.' + snsgrg + '__' + snsg + '.id}"\n')
            except KeyError:
                pass
               
            icount=len(ipcon)
            for j in range(0,icount):
                ipcname=azr[i]["properties"]["ipConfigurations"][j]["name"]
                subname=azr[i]["properties"]["ipConfigurations"][j]["properties"]["subnet"]["id"].split("/")[10].replace(".","-")
                subrg=azr[i]["properties"]["ipConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-").lower()
                #subipid=azr[i]["properties"]["ipConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[8]
                subipalloc=azr[i]["properties"]["ipConfigurations"][j]["properties"]["privateIPAllocationMethod"]
                privip=azr[i]["properties"]["ipConfigurations"][j]["properties"]["privateIPAddress"]
                prim=azr[i]["properties"]["ipConfigurations"][j]["properties"]["primary"]

                                      
                fr.write('\t ip_configuration {' + '\n')
                fr.write('\t\t name = "' + ipcname + '"\n')
                if subrg[0].isdigit(): subrg="rg_"+subrg
                fr.write('\t\t subnet_id = "${azurerm_subnet.' + subrg + '__' + subname + '.id}"\n')
                if subipalloc != "Dynamic":
                    fr.write('\t\t private_ip_address = "' + privip + '"\n')
               
                fr.write('\t\t private_ip_address_allocation = "' +    subipalloc + '"\n')
                try:
                    pubipnam=azr[i]["properties"]["ipConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[8].replace(".","-")
                    pubiprg=azr[i]["properties"]["ipConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[4].replace(".","-").lower()
                    if pubiprg[0].isdigit(): pubiprg="rg_"+pubiprg
                    fr.write('\t\t public_ip_address_id = "${azurerm_public_ip.' + pubiprg + '__' + pubipnam + '.id}"\n')
                except KeyError:
                    pass

                #fr.write('\t\t application_gateway_backend_address_pools_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t load_balancer_backend_address_pools_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t load_balancer_inbound_nat_rules_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t application_security_group_ids = "' +    subipalloc + '"\n')
                fr.write('\t\t primary = ' + str(prim).lower() + '\n')
                try:
                    asgs=azr[i]["properties"]["ipConfigurations"][j]["properties"]["applicationSecurityGroups"]
                    kcount=len(asgs)
                    for k in range(0,kcount):
                        asgnam=azr[i]["properties"]["ipConfigurations"][j]["properties"]["applicationSecurityGroups"][k]["id"].split("/")[8].replace(".","-")
                        asgrg=azr[i]["properties"]["ipConfigurations"][j]["properties"]["applicationSecurityGroups"][k]["id"].split("/")[4].replace(".","-").lower()
                        if asgrg[0].isdigit(): asgrg="rg_"+asgrg
                        fr.write('\t\t application_security_group_ids = ["${azurerm_application_security_group.' + asgrg + '__' + asgnam + '.id}"]\n')
                except KeyError:
                    pass


                fr.write('\t}\n') # end ip configurations
            # end j           

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub 
#
# azurerm_dns_zone
#
# azurerm_dns_zone
def azurerm_dns_zone(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_dns_zone"
    tcode="131-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/dnszones"
        #params = {'api-version': '2016-04-01'}
        params = {'api-version': '2018-05-01'}       
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            #loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            #fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

    ###############
    # specific code start
    ###############

            #azr=az network dns zone list -g rgsource -o json
 
            zt=azr[i]["properties"]["zoneType"]
            try:
                resvn=azr[i]["properties"]["resolutionVirtualNetworks"]
                kcount=len(resvn)
                for k in range(0,kcount):
                    vid=resvn[k]["id"]
                    fr.write('\t resolution_virtual_network_ids = ["' + vid  + '"]\n')
            except KeyError:
                pass
            try:
                regvn=azr[i]["properties"]["registrationVirtualNetworks"] 
                kcount=len(regvn)
                for k in range(0,kcount):
                    vid=regvn[k]["id"]
                    fr.write('\t registration_virtual_network_ids = "' +  regvn + '"\n') 
            except KeyError:
                pass  

            fr.write('\t zone_type = "' +  zt + '"\n')
      

    ###############
    # specific code end
    ###############

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_lb
#
# azurerm_lb
def azurerm_lb(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_lb"
    tcode="140-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Load Balancers"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/loadBalancers"
        params = {'api-version': '2019-02-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            sku=azr[i]["sku"]["name"]
            fronts=azr[i]["properties"]["frontendIPConfigurations"]
        
            fr.write('\t sku = "' +  sku + '"\n')
           
            jcount=len(fronts)
       
   
            for j in range(0,jcount):
                    
                fname=azr[i]["properties"]["frontendIPConfigurations"][j]["name"]             
                fr.write('\t frontend_ip_configuration {' + '\n')
                fr.write('\t\t name = "' +    fname + '"\n')
                try:
                    subrg=azr[i]["properties"]["frontendIPConfigurations"][j]["subnet"]["id"].split("/")[4].replace(".","-").lower()
                    subname=azr[i]["properties"]["frontendIPConfigurations"][j]["subnet"]["id"].split("/")[10].replace(".","-")
                    if subrg[0].isdigit(): subrg="rg_"+subrg
                    fr.write('\t\t subnet_id = "${azurerm_subnet.' + subrg + '__' + subname +'.id}"\n')
                except KeyError:
                    pass
               
                try:
                    priv=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["privateIPAddress"]
                    fr.write('\t\t private_ip_address = "' +    priv + '"\n')
                except KeyError:
                    pass         
                    privalloc=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["privateIPAllocationMethod"]
                    fr.write('\t\t private_ip_address_allocation  = "' + privalloc + '"\n')
                except KeyError:
                    pass
                try:
                    pubrg=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["publicAddress"]["id"].split("/")[4].replace(".","-").lower()
                    pubname=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["publicAddress"]["id"].split("/")[8].replace(".","-")
                    if pubrg[0].isdigit(): pubrg="rg_"+pubrg
                    fr.write('\t\t public_ip_address_id = "${azurerm_public_ip.' + pubrg + '__' + pubname + '.id}"\n')
                except KeyError:
                    pass

                fr.write('\t }\n')
            # end j    

    ###############
    # specific code end
    ###############

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
        
    #end stub
 
#
# azurerm_lb_nat_rule
#
# azurerm_lb_nat_rule
def azurerm_lb_nat_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_lb_nat_rule"
    tcode="150-"
    if crf in tfp:
    # REST or cli

        # print "REST Load Balancers"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/loadBalancers"
        params = {'api-version': '2019-02-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):
            try:
                beap=azr[i]["properties"]["inboundNatRules"] 
                id=azr[i]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if rg[0].isdigit(): rg="rg_"+rg
                rgs=id.split("/")[4]
                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for
                if cde:
                    print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
   
                jcount=len(beap)   
                      
                for j in range(0,jcount):
                    
                    name=azr[i]["properties"]["inboundNatRules"][j]["name"]
                    rname=name.replace(".","-")

                    id=azr[i]["properties"]["inboundNatRules"][j]["id"]
                    rg=id.split("/")[4].replace(".","-").lower()
                    if crg is not None:
                        if rgs.lower() != crg.lower():
                            continue  # back to for

                    prefix=tfp+"."+rg+'__'+rname
                    #print prefix
                    rfilename=prefix+".tf"
                    fr=open(rfilename, 'w')
                    fr.write(az2tfmess)
                       
                    lbrg=azr[i]["id"].split("/")[4].replace(".","-").lower()
                    lbname=azr[i]["id"].split("/")[8].replace(".","-")
                    if lbrg[0].isdigit(): lbrg="rg_"+lbrg 
                    fep=azr[i]["properties"]["inboundNatRules"][j]["properties"]["frontendPort"]
                    bep=azr[i]["properties"]["inboundNatRules"][j]["properties"]["backendPort"]
                    proto=azr[i]["properties"]["inboundNatRules"][j]["properties"]["protocol"]
                    feipc=azr[i]["properties"]["inboundNatRules"][j]["properties"]["frontendIPConfiguration"]["id"].split("/")[10]
                    
                    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')   

                    fr.write('\t\t name = "' +    name + '"\n')
                    fr.write('\t\t resource_group_name = "' +  rg + '"\n')
                    fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg + '__' + lbname + '.id}" \n')
                    fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')
                    fr.write('\t\t protocol = "' + proto + '"\n')
                    fr.write('\t\t backend_port = "' + str(bep) + '"\n')
                    fr.write('\t\t frontend_port = "' + str(fep) + '"\n')
                    try:
                        enfip=azr[i]["properties"]["inboundNatRules"][j]["properties"]["enableFloatingIP"]
                        fr.write('\t\t enable_floating_ip = ' + str(enfip).lower() + '\n')
                    except KeyError:
                        pass

        # no tags block       

                    fr.write('}\n') 
                    fr.close()   # close .tf file

                    if cde:
                        with open(rfilename) as f: 
                            print (f.read())

                    tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                    tfim.write('echo "importing ' + str(j) + ' of ' + str(jcount-1) + '"' + '\n')
                    tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                    tfim.write(tfcomm)  

                # end for j loop
            except KeyError:
                pass        
        # end for i

        tfrm.close()
        tfim.close()

    #end stub
 
#
# azurerm_lb_nat_pool
#
# azurerm_lb_nat_pool
def azurerm_lb_nat_pool(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_lb_nat_pool"
    tcode="160-"

    if crf in tfp:
    # REST or cli
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/loadBalancers"
        params = {'api-version': '2019-02-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):
         
            name=azr[i]["name"]
         
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
    
            beap=azr[i]["properties"]["inboundNatPools"]
            jcount= len(beap)
           
            if cde:
                print(json.dumps(beap, indent=4, separators=(',', ': ')))  
      
            
            
            for j in range(0,jcount):
                
                name=azr[i]["properties"]["inboundNatPools"][j]["name"]
                rname=name.replace(".","-")
                if cde:
                    print(json.dumps(beap, indent=4, separators=(',', ': ')))
                id=azr[i]["properties"]["inboundNatPools"][j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                rgs=id.split("/")[4]
                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for

                prefix=tfp+"."+rg+'__'+rname
                
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)

                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')

                proto=azr[i]["properties"]["inboundNatPools"][j]["properties"]["protocol"]
                bep=azr[i]["properties"]["inboundNatPools"][j]["properties"]["backendPort"]

                try:
                    feps=azr[i]["properties"]["inboundNatPools"][j]["properties"]["frontendPortStart"]
                except:
                    feps=bep
                try:
                    fepe=azr[i]["properties"]["inboundNatPools"][j]["properties"]["frontendPortEnd"]
                except:
                    fepe=bep
                
                lbrg=azr[i]["id"].split("/")[4].replace(".","-").lower()
                lbname=azr[i]["id"].split("/")[8].replace(".","-")
                if lbrg[0].isdigit(): lbrg="rg_"+lbrg 
                fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg + '__' + lbname + '.id}"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t frontend_port_start = "' +    str(feps) + '"\n')
                fr.write('\t\t frontend_port_end = "' +    str(fepe) + '"\n')
                fr.write('\t\t backend_port = "' +    str(bep) + '"\n')
                try:
                    feipc=azr[i]["properties"]["inboundNatPools"][j]["properties"]["frontendConfiguration"]["id"].split("/")[10]
                    fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')
                except KeyError:
                    fr.write('\t\t frontend_ip_configuration_name = "' +  "default" + '"\n')
                    pass


        # no tags block       


                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_lb_backend_address_pool
#
# azurerm_lb_backend_address_pool
def azurerm_lb_backend_address_pool(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_lb_backend_address_pool"
    tcode="170-"
    
    if crf in tfp:
    # REST or cli
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/loadBalancers"
        params = {'api-version': '2019-02-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            lbname=name
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            beap=azr[i]["properties"]["backendAddressPools"]       
            jcount= len(beap)
            
            for j in range(0,jcount):
                
                name=azr[i]["properties"]["backendAddressPools"][j]["name"]
                rname= name.replace(".","-")
                id=azr[i]["properties"]["backendAddressPools"][j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()

                prefix=tfp+"."+rg+'__'+lbname+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)

                fr.write('resource ' + tfp + ' ' + rg + '__' +lbname+'__'+ rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')

                try:
                    #lbrg=azr[i]["id"].split("/")[4].replace(".","-").lower()
                    #lbname=azr[i]["id"].split("/")[8].replace(".","-")   
                    lbrg=id.split("/")[4].replace(".","-").lower()
                    lbname=id.split("/")[8].replace(".","-")    
                    if lbrg[0].isdigit(): lbrg="rg_"+lbrg      
                    fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg + '__' + lbname + '.id}" \n')    
                except KeyError:
                    pass
                
        # should be more stuff in here ?


                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+lbname+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+lbname+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  

            # end for j loop
        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_lb_probe
#
# azurerm_lb_probe
def azurerm_lb_probe(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_lb_probe"
    tcode="180-"
    
    if crf in tfp:
    # REST or cli
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/loadBalancers"
        params = {'api-version': '2019-02-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))

            beap=azr[i]["properties"]["probes"]
            
            icount= len(beap)
            
            for j in range(0,icount):
                
                name=azr[i]["properties"]["probes"][j]["name"]
                rname= name.replace(".","-")
                id=azr[i]["properties"]["probes"][j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                rgs=id.split("/")[4]
                lbrg=azr[i]["id"].split("/")[4].replace(".","-").lower()
                lbname=azr[i]["id"].split("/")[8].replace(".","-")

                prefix=tfp+"."+rg+'__'+lbname+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)



                fr.write('resource ' + tfp + ' ' + rg + '__' +lbname+ '__'+ rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')
 
                np=azr[i]["properties"]["probes"][j]["properties"]["numberOfProbes"]
                port=azr[i]["properties"]["probes"][j]["properties"]["port"]
                proto=azr[i]["properties"]["probes"][j]["properties"]["protocol"]

             

                if lbrg[0].isdigit(): lbrg="rg_"+lbrg 
                fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg  + '__' + lbname + '.id}" \n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t port = "' +    str(port) + '"\n')
                try:
                    rpath=azr[i]["properties"]["probes"][j]["properties"]["requestPath"]
                    fr.write('\t\t request_path = "' +    rpath + '"\n')
                except KeyError:
                    pass
                try:
                    inter=azr[i]["properties"]["probes"][j]["properties"]["intervalInSeconds"]
                    fr.write('\t\t interval_in_seconds = "' +  str(inter) + '"\n')
                except KeyError:
                    pass    

                fr.write('\t\t number_of_probes = "' +  str(np) + '"\n')

                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+lbname+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+lbname+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  
            # end for j loop
        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_lb_rule
#
# azurerm_lb_rule
def azurerm_lb_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_lb_rule"
    tcode="190-"
    
    if crf in tfp:
    # REST or cli
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/loadBalancers"
        params = {'api-version': '2019-02-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):
            name=azr[i]["name"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
 
            beap=azr[i]["properties"]["loadBalancingRules"]   
            jcount=len(beap)
            
            for j in range(0,jcount):
                
                name=azr[i]["properties"]["loadBalancingRules"][j]["name"]
                rname= name.replace(".","-")
                id=azr[i]["properties"]["loadBalancingRules"][j] ["id"]
    
                lbrg=azr[i]["id"].split("/")[4].replace(".","-").lower()
                lbname=azr[i]["id"].split("/")[8].replace(".","-")
                prefix=tfp+"."+rg+ '__' + lbname+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + lbname + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')


     
                fep=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["frontendPort"]
                bep=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["backendPort"]
                proto=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["protocol"]
                feipc=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["frontendIPConfiguration"]["id"].split("/")[10]
                efip=str(azr[i]["properties"]["loadBalancingRules"][j]["properties"]["enableFloatingIP"]).lower()
                ld=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["loadDistribution"]
                itm=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["idleTimeoutInMinutes"]
                if lbrg[0].isdigit(): lbrg="rg_"+lbrg 
                fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg + '__' + lbname + '.id}" \n')
                fr.write('\t\t frontend_ip_configuration_name = "' + feipc + '"\n')
                fr.write('\t\t protocol = "' + proto + '"\n')   
                fr.write('\t\t frontend_port = "' + str(fep) + '"\n')
                fr.write('\t\t backend_port = "' + str(bep) + '"\n')
                
                try:
                    beadprg=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["backendAddressPool"]["id"].split("/")[4].replace(".","-").lower()
                    beadpid=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["backendAddressPool"]["id"].split("/")[10].replace(".","-")
                    if beadprg[0].isdigit(): beadprg="rg_"+beadprg
                    fr.write('\t\t backend_address_pool_id = "${azurerm_lb_backend_address_pool.' + beadprg + '__' + lbname + '__' + beadpid + '.id}"\n')
                except KeyError:
                    pass
                
                try:
                    prg=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["probe"]["id"].split("/")[4].replace(".","-").lower()
                    pid=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["probe"]["id"].split("/")[10].replace(".","-")
                    if prg[0].isdigit(): prg="rg_"+prg 
                    fr.write('\t\t probe_id = "${azurerm_lb_probe.' + prg + '__' + lbname + '__' + pid + '.id}" \n')
                except KeyError:
                    pass
                fr.write('\t\t enable_floating_ip = ' + efip + '\n')
                fr.write('\t\t idle_timeout_in_minutes = "' + str(itm) + '"\n')
                fr.write('\t\t load_distribution = "' + ld + '"\n')


                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+ '__' + lbname+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+ '__' + lbname+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_application_gateway
#
# azurerm_application_gateway
def azurerm_application_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_application_gateway"
    tcode="193-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/applicationGateways"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')


            skun=azr[i]["properties"]["sku"]["name"]
           
            skut=azr[i]["properties"]["sku"]["tier"]
            
            
            # the blocks
            gwipc=azr[i]["properties"]["gatewayIPConfigurations"]
            feps=azr[i]["properties"]["frontendPorts"]
            fronts=azr[i]["properties"]["frontendIPConfigurations"]
            beap=azr[i]["properties"]["backendAddressPools"]
            bhttps=azr[i]["properties"]["backendHttpSettingsCollection"]
            httpl=azr[i]["properties"]["httpListeners"]
            probes=azr[i]["properties"]["probes"]
            rrrs=azr[i]["properties"]["requestRoutingRules"]
            urlpm=azr[i]["properties"]["urlPathMaps"]
            
            sslcerts=azr[i]["properties"]["sslCertificates"]
            #wafc=azr[i]["properties"]["webApplicationFirewallConfiguration"]

            fr.write('sku { \n')
            fr.write('\t name = "' +  skun + '"\n')
            try :
                skuc=azr[i]["properties"]["sku"]["capacity"]
                fr.write('\t capacity = "' +  str(skuc) + '"\n')
            except KeyError:
                fr.write('\t capacity = "' + '1'  + '"\n')
                pass

            fr.write('\t tier = "' +  skut + '"\n')
            fr.write('} \n')



            icount=len(gwipc)
            for j in range(0,icount):
                gname=azr[i]["properties"]["gatewayIPConfigurations"][j]["name"]
                subrg=azr[i]["properties"]["gatewayIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-").lower()
                subname=azr[i]["properties"]["gatewayIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[10].replace(".","-")
                fr.write('gateway_ip_configuration {' + '\n')
                fr.write('\t name = "' + gname + '"\n')
                try:
                    subrg=azr[i]["properties"]["gatewayIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-").lower()
                    subname=azr[i]["properties"]["gatewayIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[10].replace(".","-")
                    if subrg[0].isdigit(): subrg="rg_"+subrg
                    fr.write('\t subnet_id = "${azurerm_subnet.' + subrg + '__' + subname + '.id}" \n')
                except KeyError:  
                    pass
                fr.write('}\n')
                
        
            
    # front end port
            icount=len(feps)
            if icount > 0 :
                for j in range(0,icount):
                    fname=azr[i]["properties"]["frontendPorts"][j]["name"]
                    fport=azr[i]["properties"]["frontendPorts"][j]["properties"]["port"]
                    fr.write('frontend_port {\n')
                    fr.write('\t name = "' + fname + '"\n')
                    fr.write('\t port = "' + str(fport) + '"\n')
                    fr.write('}\n')
                
        
            
    # front end IP config block
            icount=len(fronts)
            if icount > 0 :
                for j in range(0,icount):
                    
                    fname=azr[i]["properties"]["frontendIPConfigurations"][j]["name"]
                    fr.write('frontend_ip_configuration {\n')
                    fr.write('\t name = "' + fname + '"\n')
                    try :
                        subrg=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-").lower()
                        subname=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[10].replace(".","-")                 
                        if subrg[0].isdigit(): subrg="rg_"+subrg
                        fr.write('\t subnet_id = "${azurerm_subnet.' + subrg + '__'  + subname + '.id}" \n')
                    except KeyError:
                        pass

                    try :
                        priv=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["privateIPAddress"]
                        fr.write('\t private_ip_address = "' + priv + '"\n')
                    except KeyError:
                        pass
                
                    try :
                        privalloc=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["privateIPAllocationMethod"]
                        fr.write('\t private_ip_address_allocation  = "' + privalloc + '"\n')
                    except KeyError:
                        pass

                    try :
                        pubrg=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[4].replace(".","-").lower()
                        pubname=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[8].replace(".","-")  
                        if pubrg[0].isdigit(): pubrg="rg_"+pubrg
                        fr.write('\t public_ip_address_id = "${azurerm_public_ip.' + pubrg + '__' + pubname + '.id}" \n')
                    except KeyError:
                        pass
                    
                    fr.write('}\n')
                    
                
        

    # backend_address_pool          beap=azr[i]["backendAddressPools"

            icount=len(beap)
            if icount > 0:
                for j in range(0,icount):
                    bname=azr[i]["properties"]["backendAddressPools"][j]["name"]
                    fr.write('backend_address_pool {' + '\n')
                    fr.write('\t name = "' + bname + '"\n')
                    beaddr=azr[i]["properties"]["backendAddressPools"][j]["properties"]["backendAddresses"]         
                    kcount=len(beaddr)    
                    if kcount > 0 :
                        for k in range(0,kcount):       
                            try :
                                beadip=azr[i]["properties"]["backendAddressPools"][j]["properties"]["backendAddresses"][k]["IPAddress"]
                                fr.write('\t ip_address ="' +  beadip + '"\n')
                            except KeyError:
                                pass
                            try:
                                beadfq=azr[i]["properties"]["backendAddressPools"][j]["properties"]["backendAddresses"][k]["fqdn"]
                                fr.write('\t fqdns = ["' + beadfq + '"] \n')         
                            except KeyError:
                                pass
                    fr.write('}\n')
                

    # backend_http_settings
            icount=len(bhttps)
            if icount > 0:
                for j in range(0,icount):
                    bname=azr[i]["properties"]["backendHttpSettingsCollection"][j]["name"]
                    bport=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["port"]
                    bproto=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["protocol"]
                    bcook=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["cookieBasedAffinity"]
                    btimo=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["requestTimeout"]
                    #pname=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["probe"]["id"].split("/")[10]
                    
                    fr.write('backend_http_settings {\n')
                    fr.write('\t name = "' + bname + '"\n')
                    fr.write('\t port = "' + str(bport) + '"\n')
                    fr.write('\t protocol = "' + bproto + '"\n')
                    fr.write('\t cookie_based_affinity = "' + bcook + '"\n')
                    fr.write('\t request_timeout = "' + str(btimo) + '"\n')
                    try :
                        pname=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["probe"]["id"].split("/")[10]
                        fr.write('\t probe_name = "' + pname + '"\n')
                    except KeyError:
                        pass
                    try :
                        bhn=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["hostName"]
                        try:
                            fr.write('\t host_name = "' + bhn + '"\n')
                        except TypeError:
                            pass
                    except KeyError:
                        pass               
                   
                    try :
                        acert=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["authenticationCertificates"][0]["id"].split("/")[10]
                        #print acert
                        fr.write('\t authentication_certificate { \n')
                        fr.write('\t\t name = "' + acert + '"\n')
                        fr.write('\t}\n')
                    except KeyError:
                        pass
                    fr.write('}\n')
                
            
            
    # http listener block          httpl=azr[i]["httpListeners"

            icount=len(httpl)
            if icount > 0:
                for j in range(0,icount):
                    bname=azr[i]["properties"]["httpListeners"][j]["name"]
                    feipcn=azr[i]["properties"]["httpListeners"][j]["properties"]["frontendIPConfiguration"]["id"].split("/")[10]
                    fepn=azr[i]["properties"]["httpListeners"][j]["properties"]["frontendPort"]["id"].split("/")[10]
                    bproto=azr[i]["properties"]["httpListeners"][j]["properties"]["protocol"]
                                                                     

                    fr.write('http_listener {\n')
                    fr.write('\t name = "' +    bname + '"\n')
                    fr.write('\t frontend_ip_configuration_name = "' +    feipcn + '"\n')
                    fr.write('\t frontend_port_name = "' +    fepn + '"\n')
                    fr.write('\t protocol = "' +    bproto + '"\n')
                    try :
                        bhn=azr[i]["properties"]["httpListeners"][j]["properties"]["hostName"]
                        fr.write('\t host_name = "' +    bhn + '"\n')
                    except KeyError:
                        pass
                    try :
                        bssl=azr[i]["properties"]["httpListeners"][j]["properties"]["sslCertificate"]["id"].split("/")[10]
                        fr.write('\t ssl_certificate_name = "' +    bssl + '"\n')
                    except KeyError:
                        pass
                    try :
                        rsni=azr[i]["properties"]["httpListeners"][j]["properties"]["requireServerNameIndication"]
                        fr.write('\t require_sni = ' +  str(rsni).lower() + '\n')
                    except KeyError:
                        pass
                    fr.write('}\n')
                
# probe block

            icount=len(probes)
            if icount > 0 :
                for j in range(0,icount):
                    bname=azr[i]["properties"]["probes"][j]["name"]
                    bproto=azr[i]["properties"]["probes"][j]["properties"]["protocol"]
                    bpath=azr[i]["properties"]["probes"][j]["properties"]["path"]
                    bint=azr[i]["properties"]["probes"][j]["properties"]["interval"]
                    btimo=azr[i]["properties"]["probes"][j]["properties"]["timeout"]
                    bunth=azr[i]["properties"]["probes"][j]["properties"]["unhealthyThreshold"]
                                   
                                
                    #bmstat=azr[i]["properties"]["probes"][j]["properties"]["match"]["statusCodes"]

                    fr.write('probe {' + '\n')
                    fr.write('\t name = "' +    bname + '"\n')
                    fr.write('\t protocol = "' +    bproto + '"\n')
                    fr.write('\t path = "' +    bpath + '"\n')
                    try:
                        bhost=azr[i]["properties"]["probes"][j]["properties"]["host"]
                        fr.write('\t host = "' +    bhost + '"\n')
                    except KeyError:
                        pass
                    fr.write('\t interval = "' +  str(bint) + '"\n')
                    fr.write('\t timeout = "' +    str(btimo) + '"\n')
                    fr.write('\t unhealthy_threshold = "' +  str(bunth) + '"\n')


                    try :
                        bmsrv=azr[i]["properties"]["probes"][j]["properties"]["minServers"]
                        fr.write('\t minimum_servers = "' + str(bmsrv) + '"\n')
                    except KeyError:
                        pass

                    fr.write('\t match {' + '\n')
                    
                    try :
                        bmbod=azr[i]["properties"]["probes"][j]["properties"]["match"]["body"] 
                        if bmbod == "":
                            fr.write('\t\t body = "' + '*' + '"\n')
                        else:
                            fr.write('\t\t body = "' + bmbod + '"\n')
                    except KeyError:
                        pass
                
                    fr.write('\t }\n')
                    fr.write('}\n')
                    

# routing rules

            icount=len(rrrs)
            if icount > 0 :
                for j in range(0,icount):
                    bname=azr[i]["properties"]["requestRoutingRules"][j]["name"]
                    btyp=azr[i]["properties"]["requestRoutingRules"][j]["properties"]["ruleType"]
                    blin=azr[i]["properties"]["requestRoutingRules"][j]["properties"]["httpListener"]["id"].split("/")[10]

                    fr.write('request_routing_rule { \n')

                    fr.write('\t name = "' + bname + '"\n')
                    fr.write('\t rule_type = "' + btyp + '"\n')
                    fr.write('\t http_listener_name = "' + blin + '"\n')
                    try :
                        bapn=azr[i]["properties"]["requestRoutingRules"][j]["properties"]["backendAddressPool"]["id"].split("/")[10]
                        fr.write('\t backend_address_pool_name = "' +    bapn + '"\n')
                    except KeyError:
                        pass
                    try :
                        bhsn=azr[i]["properties"]["requestRoutingRules"][j]["properties"]["backendHttpSettings"]["id"].split("/")[10]
                        fr.write('\t backend_http_settings_name = "' +    bhsn + '"\n')
                    except KeyError:
                        pass
                    fr.write('\t }\n')
                
        


    # ssl_certificate block   sslcerts=azr[i]["sslCertificates"

            jcount=len(sslcerts)
            if jcount > 0 :
                for j in range(0,jcount):
                    #print "***********"
                    #print(json.dumps(sslcerts[j], indent=4, separators=(',', ': ')))

                    try :
                        bname=azr[i]["properties"]["sslCertificates"][j]["name"]
                        fr.write('ssl_certificate {' + '\n')
                        fr.write('\t name = "' + bname + '"\n')


                        try :
                            bdata=azr[i]["properties"]["sslCertificates"][j]["properties"]["dummy"]
                            fr.write('\t data = "' + bdata + '"\n')
                        except KeyError:
                            fr.write('\t data = ""\n') 
                            pass
                        
                        try :
                            bpw=azr[i]["properties"]["sslCertificates"][j]["password"]
                            fr.write('\t password = "' + bpw + '"\n')       
                        except KeyError:
                            fr.write('\t password = ""\n')
                            pass




                        fr.write('\t }\n')

                    except KeyError:
                        pass
                
                
        

    # waf configuration block     wafc=azr[i]["webApplicationFirewallConfiguration"]
    # - not an array like the other blocks 
    #
            
            try :
                fmode=azr[i]["properties"]["webApplicationFirewallConfiguration"]["firewallMode"]
                rst=azr[i]["properties"]["webApplicationFirewallConfiguration"]["ruleSetType"]
                rsv=azr[i]["properties"]["webApplicationFirewallConfiguration"]["ruleSetVersion"]
                fen=azr[i]["properties"]["webApplicationFirewallConfiguration"]["enabled"]
                    
                fr.write('waf_configuration { \n')
                fr.write('\t firewall_mode = "' + fmode + '"\n')
                fr.write('\t rule_set_type = "' + rst + '"\n')
                fr.write('\t rule_set_version = "' + rsv + '"\n')
                fr.write('\t enabled = ' + str(fen).lower() + '\n')
                fr.write('\t }\n') 
            except KeyError:
                pass         
            
            #if cde:
            #    print(json.dumps(authcerts, indent=4, separators=(',', ': ')))
            try:
                authcerts=azr[i]["properties"]["authenticationCertificates"]
                jcount=len(authcerts)
                for j in range(0,jcount):
                    cname=azr[i]["properties"]["authenticationCertificates"][j]["name"]
                    cdata=azr[i]["properties"]["authenticationCertificates"][j]["properties"]["data"]
                    fr.write('authentication_certificate {\n')
                    fr.write('\t name = "' + cname + '"\n')  
                    fr.write('\t data = "' + '"\n') 
                    fr.write('\t }\n')
            except KeyError:
                pass

  
    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

 
#
# azurerm_local_network_gateway
#
# azurerm_local_network_gateway
import ast
def azurerm_local_network_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_local_network_gateway"
    tcode="200-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Local NW Gateway"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/localNetworkGateways"
        params = {'api-version': '2019-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr=r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

  

            gwaddr=azr[i]["properties"]["gatewayIpAddress"]

            try:
                addrpre=str(ast.literal_eval(json.dumps(azr[i]["properties"]["localNetworkAddressSpace"]["addressPrefixes"])))
                addrpre=addrpre.replace("'",'"')
                if "[]" not in addrpre:
                    fr.write('\t address_space =  ' + addrpre +  '\n')
            except KeyError:
                pass
            
            fr.write('\t gateway_address = "' +  gwaddr + '"\n')
            
        
            try :
                bgps=azr[i]["properties"]["bgpSettings"]
                asn=azr[i]["properties"]["bgpSettings"]["asn"]
                peera=azr[i]["properties"]["bgpSettings"]["bgpPeeringAddress"]
                peerw=azr[i]["properties"]["bgpSettings"]["peerWeight"]

                fr.write('\t bgp_settings {\n')
                fr.write('\t\t asn = "' + str(asn) + '"\n')
                fr.write('\t\t bgp_peering_address = "' + peera + '"\n')
                fr.write('\t\t peer_weight = "' + str(peerw) + '"\n')
                fr.write('\t } \n')
            except KeyError:
                pass
        

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_virtual_network_gateway
#
# azurerm_virtual_network_gateway
import ast
def azurerm_virtual_network_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_virtual_network_gateway"
    tcode="210-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/virtualNetworkGateways"
        params = {'api-version': '2019-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            gtype=azr[i]["properties"]["gatewayType"]
            vpntype=azr[i]["properties"]["vpnType"]

            sku=azr[i]["properties"]["sku"]["name"]
                       
            aa=azr[i]["properties"]["activeActive"]
            enbgp=azr[i]["properties"]["enableBgp"]
            
            fr.write('\t vpn_type = "' +  vpntype + '"\n')
            fr.write('\t type = "' + gtype + '"\n')
            try:
                sku=azr[i]["properties"]["sku"]["name"]        
                fr.write('\t sku = "' +  sku + '"\n')
            except KeyError:
                pass
            
            
            fr.write('\t active_active = "' + str(aa).lower() + '"\n')
            fr.write('\t enable_bgp = "' + str(enbgp).lower() + '"\n')
            
            try :
                vadsp=str(ast.literal_eval(json.dumps(azr[i]["properties"]["vpnClientConfiguration"]["vpnClientAddressPool"]["addressPrefixes"])))
                vadsp=vadsp.replace("'",'"')
                fr.write('\t vpn_client_configuration {\n')
                fr.write('\t\t address_space = ' + vadsp + '\n')
                try:
                    radsa=azr[i]["properties"]["vpnClientConfiguration"]["radiusServerAddress"]
                    radss=azr[i]["properties"]["vpnClientConfiguration"]["radiusServerSecret"]
                    fr.write('\t\t radius_server_address = "' + radsa + '"\n')
                    fr.write('\t\t radius_server_secret = "' + radss + '"\n')
                except KeyError:  # = null
                    fr.write('\t\t root_certificate { \n')
                    fr.write('\t\t\t name = ""\n')
                    fr.write('\t\t\t public_cert_data = ""\n')
                    fr.write('\t\t }\n')
                    pass
            
                try :
                    vcp=str(ast.literal_eval(json.dumps(azr[i]["properties"]["vpnClientConfiguration"]["vpnClientProtocols"])))
                    vcp=vcp.replace("'",'"')
                    fr.write('\t\t vpn_client_protocols = ' + vcp + '\n')
                except KeyError:
                    pass            
                
                fr.write('\t }\n')
            except KeyError:
                pass
        
            try :
                bgps=azr[i]["properties"]["bgpSettings"]
                fr.write('\t bgp_settings {\n')
                asn=azr[i]["properties"]["bgpSettings"]["asn"]
                peera=azr[i]["properties"]["bgpSettings"]["bgpPeeringAddress"]
                peerw=azr[i]["properties"]["bgpSettings"]["peerWeight"]
                fr.write('\t\t asn = "' +  str(asn) + '"\n')
                fr.write('\t\t peering_address = "' + peera + '"\n')
                fr.write('\t\t peer_weight = "' + str(peerw) + '"\n')
                fr.write('\t } \n')
            except KeyError:
                pass
        
            
            ipc=azr[i]["properties"]["ipConfigurations"]
            count= len(ipc)
            for j in range(0,count):
                ipcname= ipc[j]["name"]
                ipcpipa= ipc[j]["properties"]["privateIPAllocationMethod"]
                
                fr.write('\tip_configuration {\n')
                fr.write('\t\t name = "' + ipcname + '"\n')
                fr.write('\t\t private_ip_address_allocation = "' + ipcpipa + '"\n')
                try :
                    ipcpipid= ipc[j]["properties"]["publicIPAddress"]["id"]
                    pipnam= ipcpipid.split("/")[8].replace(".","-")
                    piprg= ipcpipid.split("/")[4].replace(".","-").lower()
                    if piprg[0].isdigit(): piprg="rg_"+piprg
                    fr.write('\t\t public_ip_address_id = "${azurerm_public_ip.' + piprg + '__' + pipnam + '.id}"\n')
                except KeyError:
                    pass

                try :
                    ipcsubid= ipc[j]["properties"]["subnet"]["id"]
                    subnam= ipcsubid.split("/")[10].replace(".","-")
                    subrg= ipcsubid.split("/")[4].replace(".","-").lower()
                    if subrg[0].isdigit(): subrg="rg_"+subrg
                    fr.write('\t\t subnet_id = "${azurerm_subnet.' + subrg + '__' + subnam + '.id}"\n')
                except KeyError:
                    pass
                fr.write('\t}\n')
        

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_virtual_network_gateway_connection
#
# azurerm_virtual_network_gateway_connection
def azurerm_virtual_network_gateway_connection(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_virtual_network_gateway_connection"
    tcode="220-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/connections"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

    ##  azr=az network vpn-connection list -g rgsource -o json
        
            ctype=azr[i]["properties"]["connectionType"]
            vngrg=azr[i]["properties"]["virtualNetworkGateway1"]["id"].split("/")[4].replace(".","-").lower()
            vngnam=azr[i]["properties"]["virtualNetworkGateway1"]["id"].split("/")[8].replace(".","-")
            

            
            if ctype == "IPsec" :
                
                peerrg=azr[i]["properties"]["localNetworkGateway2"]["id"].split("/")[4].replace(".","-").lower()
                peernam=azr[i]["properties"]["localNetworkGateway2"]["id"].split("/")[8].replace(".","-")
    
            

            enbgp=azr[i]["properties"]["enableBgp"]
            rw=azr[i]["properties"]["routingWeight"]

            pbs=azr[i]["properties"]["usePolicyBasedTrafficSelectors"]
            
            fr.write('\t type = "' +  ctype + '"\n')
            if vngrg[0].isdigit(): vngrg="rg_"+vngrg
            fr.write('\t\t virtual_network_gateway_id = "${azurerm_virtual_network_gateway.' + vngrg + '__' + vngnam + '.id}"\n')
            try:
                authkey=azr[i]["properties"]["authorizationKey"]
                fr.write('\t authorization_key = "' +  authkey + '"\n')
            except KeyError:
                pass
        
            
            fr.write('\t enable_bgp = ' +  str(enbgp).lower() + '\n')
            try:
                rw=azr[i]["properties"]["routingWeight"] 
                if rw != 0 :
                    fr.write('\t routing_weight = "' + str(rw) + '"\n')
            except KeyError:
                pass

            try :
                sk=azr[i]["properties"]["shared_key"]
                fr.write('\t shared_key = "' +  sk + '"\n')
            except KeyError:
                pass   


            fr.write('\t use_policy_based_traffic_selectors = ' + str(pbs).lower() + '\n')
            
            if ctype == "ExpressRoute" :
                peerid=azr[i]["properties"]["peer"]["id"]
                fr.write('\t\t express_route_circuit_id = "' +  peerid + '"\n')
                #fr.write('\t\t express_route_circuit_id = "${azurerm_virtual_network_gateway. + '__' + .id}'"' peerrg peernam + '"\n')
                peerid=azr[i]["properties"]["peer"]["id"]
                peerrg=peerid.split("/")[4].replace(".","-").lower()
                if peerrg[0].isdigit(): peerrg="rg_"+peerrg
                peernam=peerid.split("/")[8].replace(".","-")
        
            if ctype == "Vnet2Vnet" :
                fr.write('\t peer_virtual_network_gateway_id = "${azurerm_virtual_network_gateway.' + peerrg +'__' + peernam + '.id}"\n')
        
            if ctype == "IPsec" :
                fr.write('\t local_network_gateway_id = "${azurerm_local_network_gateway.' + peerrg + '__' + peernam + '.id}" \n')
        
            
            
            ipsec=azr[i]["properties"]["ipsecPolicies"]
            jcount= len(ipsec)
            if jcount > 0 :
                for j in range(0,jcount):
                    fr.write('\t ipsec_policy {' + '\n')
                    dhg= ipsec[j]["dhGroup"]
                    ikee= ipsec[j]["ikeEncryption"]
                    ikei= ipsec[j]["ikeIntegrity"]
                    ipsece= ipsec[j]["ipsecEncryption"]
                    ipseci= ipsec[j]["ipsecIntegrity"]
                    pfsg= ipsec[j]["pfsGroup"]
                    sadata= ipsec[j]["saDataSizeKilobytes"]
                    salife= ipsec[j]["saLifeTimeSeconds"]
                    fr.write('\t dh_group = "' + dhg + '"\n')
                    fr.write('\t ike_encryption = "' + ikee + '"\n')
                    fr.write('\t ike_integrity = "' + ikei + '"\n')
                    fr.write('\t ipsec_encryption = "' + ipsece + '"\n')
                    fr.write('\t ipsec_integrity = "' + ipseci + '"\n')
                    fr.write('\t pfs_group = "' + pfsg + '"\n')
                    fr.write('\t sa_datasize = "' + str(sadata) + '"\n')
                    fr.write('\t sa_lifetime = "' + str(salife) + '"\n')
                    fr.write('\t}\n')
                
    
    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_express_route_circuit
#
# azurerm_express_route_circuit
def azurerm_express_route_circuit(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_express_route_circuit"
    tcode="230-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers//Microsoft.Network/expressRouteCircuits"
        params = {'api-version': '2018-01-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            tier=azr[i]["sku"]["tier"]
            family=azr[i]["sku"]["family"]
            aco=azr[i]["properties"]["allowClassicOperations"]
            sp=azr[i]["properties"]["serviceProviderProperties"]["serviceProviderName"]
            pl=azr[i]["properties"]["serviceProviderProperties"]["peeringLocation"]
            bw=azr[i]["properties"]["serviceProviderProperties"]["bandwidthInMbps"]
            
            
            fr.write('\t service_provider_name = "' + sp + '"\n')
            fr.write('\t peering_location = "' + pl + '"\n')
            fr.write('\t bandwidth_in_mbps = "' + str(bw) + '"\n')
            
            fr.write('\t sku {'   + '\n')
            fr.write('\t\t tier = "' +  tier + '"\n')
            fr.write('\t\t family = "' +  family + '"\n')
            fr.write('\t }\n')

            fr.write('\t allow_classic_operations = ' +  str(aco).lower() + '\n')


    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_express_route_circuit_authorization
#
# azurerm_express_route_circuit_authorization
def azurerm_express_route_circuit_authorization(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_express_route_circuit_authorization"
    tcode="240-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/expressRouteCircuits"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            name2=name
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)

            
            auths=azr[i]["properties"]["authorizations"]            
            acount= len(auths)
            if acount > 0 :
                for k in range(0,acount):
                
                    name=auths[k]["name"]
                    id= auths[k]["id"]
                    
                    rname= name.replace(".","-")

                    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                    fr.write('\t name = "' + name + '"\n')
                    fr.write('\t resource_group_name = "'+ rgs + '"\n')
               
                    fr.write('\t express_route_circuit_name = "' +  name2 + '"\n')                                  

                    fr.write('}\n')
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_express_route_circuit_peering
#
# azurerm_express_route_circuit_peering
import ast
def azurerm_express_route_circuit_peering(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_express_route_circuit_peering"
    tcode="250-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/expressRouteCircuits"
        params = {'api-version': '2018-01-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            name2=name
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            peers=azr[i]["properties"]["peerings"]          
            acount=len(peers)
           
            for k in range(0,acount):
                
                name=peers[k]["name"]
                id= peers[k]["id"]
                rname=name.replace(".","-")

                id=azr[i]["id"]
                

                prefix=tfp+"."+rg+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                #fr.write('\t name = "' + name + '"\n')
                #fr.write('\t location = "'+ loc + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')

                pt= peers[k]["properties"]["peeringType"]
                pap= peers[k]["properties"]["primaryPeerAddressPrefix"]
                sap= peers[k]["properties"]["secondaryPeerAddressPrefix"]
                vid= peers[k]["properties"]["vlanId"]
                pasn= peers[k]["properties"]["peerASN"]
            

                fr.write('\t peering_type = "' +  pt + '"\n')
                fr.write('\t express_route_circuit_name = "' +  name2 + '"\n')
                #fr.write('\t resource_group_name = "' +  rg + '"\n')
                fr.write('\t primary_peer_address_prefix = "' +  pap + '"\n')
                fr.write('\t secondary_peer_address_prefix = "' +  sap + '"\n')
                fr.write('\t vlan_id = "' +  str(vid) + '"\n')
                #fr.write('\t shared_key = "' +  sk + '"\n')
                fr.write('\t peer_asn = "' +  str(pasn) + '"\n')
                

                if pt == "MicrosoftPeering" or pt == "AzurePrivatePeering":
                    try:
                        app=str(ast.literal_eval(json.dumps(peers[k]["properties"]["microsoftPeeringConfig"]["advertisedPublicPrefixes"])))
                        app=app.replace("'",'"')

                        fr.write('\t microsoft_peering_config {' + '\n')
                        fr.write('\t\t advertised_public_prefixes =  ' + app + ' \n')
                        fr.write('\t }'  + '\n')
                    except KeyError:
                        pass

    # no tags        

                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm) 

            # end k loop

        # end for i loop
        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_container_registry
#
# azurerm_container_registry
def azurerm_container_registry(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_container_registry"
    tcode="260-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.ContainerRegistry/registries"
        params = {'api-version': '2017-10-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')
            admin=azr[i]["properties"]["adminUserEnabled"]
            sku=azr[i]["sku"]["name"]
            
            fr.write('\t admin_enabled = ' + str(admin).lower() + '\n')
            fr.write('\t sku = "' + sku + '"\n')
        
  

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_kubernetes_cluster
#
# azurerm_kubernetes_cluster
def azurerm_kubernetes_cluster(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_kubernetes_cluster"
    tcode="270-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.ContainerService/managedClusters"
        params = {'api-version': '2019-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

    ###############
    # specific code start
    ###############

            #admin=azr[i]["adminUserEnabled"]
            
            dnsp=azr[i]["properties"]["dnsPrefix"]
            rbac=azr[i]["properties"]["enableRBAC"]
            kv=azr[i]["properties"]["kubernetesVersion"]
            

            #vnsrg=azr[i]["properties"]["agentPoolProfiles"][0]["vnetSubnetId"].split("/")[4].lower()
            #vnsid=azr[i]["properties"]["agentPoolProfiles"][0]["vnetSubnetId"].split("/")[10]
           
            

            fr.write('\t dns_prefix = "' +  dnsp + '"\n')
            fr.write('\t kubernetes_version = "' +  kv + '"\n')
            
            if rbac == "true" :
                fr.write('\t role_based_access_control { \n')
                fr.write('\t\t enabled = true \n')
                fr.write('\t }\n')
        
            
            try :
                lp=azr[i]["properties"]["linuxProfile"]
                au=azr[i]["properties"]["linuxProfile"]["adminUsername"]
                sshk=azr[i]["properties"]["linuxProfile"]["ssh"]["publicKeys"][0]["keyData"]

                fr.write('\t linux_profile {\n')
                fr.write('\t\t admin_username =  "' +  au + '"\n')
                fr.write('\t\t ssh_key {\n')
                fr.write('\t\t\t key_data = "' + sshk.rstrip() + '"\n')
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
                np=azr[i]["properties"]["networkProfile"]
                netp=azr[i]["properties"]["networkProfile"]["networkPlugin"]
                srvcidr=azr[i]["properties"]["networkProfile"]["serviceCidr"]
                dnssrvip=azr[i]["properties"]["networkProfile"]["dnsService"]
                dbrcidr=azr[i]["properties"]["networkProfile"]["dockerBridgeCidr"]
                podcidr=azr[i]["properties"]["networkProfile"]["podCidr"]

                fr.write('\t network_profile {\n')
                fr.write('\t\t network_plugin =  "' +  netp + '"\n')
                try :
                    srvcidr=azr[i]["properties"]["networkProfile"]["serviceCidr"]
                    fr.write('\t\t service_cidr =  "' +  srvcidr + '"\n')
                except KeyError:
                    pass
            
                try :
                    dnssrvip=azr[i]["properties"]["networkProfile"]["dnsService"]
                    fr.write('\t\t dns_service_ip =  "' +  dnssrvip + '"\n')
                except KeyError:
                    pass
            
                try :
                    dbrcidr=azr[i]["properties"]["networkProfile"]["dockerBridgeCidr"]
                    fr.write('\t\t docker_bridge_cidr =  "' +  dbrcidr + '"\n')
                except KeyError:
                    pass
            
                try :
                    podcidr=azr[i]["properties"]["networkProfile"]["podCidr"]
                    fr.write('\t\t pod_cidr =  "' +  podcidr + '"\n')
                except KeyError:
                    pass

                fr.write('\t }\n')
            
            except KeyError:
                    pass

            try:
                pname=azr[i]["properties"]["agentPoolProfiles"][0]["name"]
                vms=azr[i]["properties"]["agentPoolProfiles"][0]["vmSize"]
                pcount=azr[i]["properties"]["agentPoolProfiles"][0]["count"]
                ost=azr[i]["properties"]["agentPoolProfiles"][0]["osType"]


                fr.write('\t agent_pool_profile {\n')
                fr.write('\t\t name =  "' + pname + '"\n')
                fr.write('\t\t vm_size =  "' + vms + '"\n')
                fr.write('\t\t count =  "' + str(pcount) + '"\n')
                fr.write('\t\t os_type =  "' + ost + '"\n')

                try :
                    vnsrg=azr[i]["properties"]["agentPoolProfiles"][0]["vnetSubnetId"].split("/")[4].lower()
                    vnsid=azr[i]["properties"]["agentPoolProfiles"][0]["vnetSubnetId"].split("/")[10]
                    if vnsrg[0].isdigit(): vnsrg="rg_"+vnsrg
                    fr.write('\t\t vnet_subnet_id = "${azurerm_subnet.' + vnsrg + '__' + vnsid + '.id}" \n')      
                except KeyError:
                    pass

                fr.write('\t }\n')
            except KeyError:
                pass

            try:
                clid=azr[i]["properties"]["servicePrincipalProfile"]["clientId"]
                fr.write('\t service_principal { \n')
                fr.write('\t\t client_id =  "' +  clid + '"\n')
                fr.write('\t\t client_secret =  "ChangeME"\n')
                fr.write('\t }\n')
            except KeyError:
                pass


    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_recovery_services_vault
#
# azurerm_recovery_services_vault
def azurerm_recovery_services_vault(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_recovery_services_vault"
    tcode="280-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.RecoveryServices/vaults"
        params = {'api-version': '2018-07-10'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            sku=azr[i]["sku"]["name"]

            fr.write('\t sku = "' +  sku + '"\n')
        
    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_virtual_machine
#
# azurerm_virtual_machine
def azurerm_virtual_machine(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_virtual_machine"
    tcode="290-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/virtualMachines"
        params = {'api-version': '2019-03-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for

            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')
        
            
            
            vmtype=azr[i]["properties"]["storageProfile"]["osDisk"]["osType"]
            vmsize=azr[i]["properties"]["hardwareProfile"]["vmSize"]
            #vmdiags=azr[i]["properties"]["diagnosticsProfile"]
            #vmbturi=azr[i]["properties"]["diagnosticsProfile"]["bootDiagnostics"]["storageUri"]
            netifs=azr[i]["properties"]["networkProfile"]["networkInterfaces"]
            datadisks=azr[i]["properties"]["storageProfile"]["dataDisks"]


    

            try : 
                avsid=azr[i]["properties"]["availabilitySet"]["id"].split("/")[8].replace(".","-").lower()
                avsrg=azr[i]["properties"]["availabilitySet"]["id"].split("/")[4].replace(".","-").lower()
                if avsrg[0].isdigit(): avsrg="rg_"+avsrg
                fr.write('\t availability_set_id = "${azurerm_availability_set.' + avsrg + '__' +avsid + '.id}"\n')
            except KeyError:
                pass


            try : 
                vmlic=azr[i]["properties"]["licenseType"]
                fr.write('\t license_type = "' +  vmlic + '"\n')
            except KeyError:
                pass

            fr.write('\t vm_size = "' + vmsize + '"\n')
            #
            # Multiples
            #
            icount=len(netifs)
            priif=""
            if icount > 0 :
                fr.write('\t network_interface_ids = [\n')
                for j in range(0,icount):
                    vmnetpri=False
                    vmnetid=azr[i]["properties"]["networkProfile"]["networkInterfaces"][j]["id"].split("/")[8].replace(".","-")
                    vmnetrg=azr[i]["properties"]["networkProfile"]["networkInterfaces"][j]["id"].split("/")[4].replace(".","-").lower()
                    if vmnetrg[0].isdigit(): vmnetrg="rg_"+vmnetrg
                    try:
                        vmnetpri=azr[i]["properties"]["networkProfile"]["networkInterfaces"][j]["properties"]["primary"]
                        priif='\t primary_network_interface_id = "${azurerm_network_interface.' + vmnetrg + '__' +  vmnetid + '.id}"\n'
                    except KeyError:
                        pass
                    fr.write('\t "${azurerm_network_interface.' + vmnetrg + '__' + vmnetid + '.id}",')
                    if vmnetpri :
                        priif='\t primary_network_interface_id = "${azurerm_network_interface.' + vmnetrg + '__' +  vmnetid + '.id}"\n'
                        #print "priif="+priif    
                fr.write('\t]\n')
                fr.write(priif) 
            #
            fr.write('\t delete_data_disks_on_termination = "'+ 'false' + '"\n')
            fr.write('\t delete_os_disk_on_termination = "'+ 'false' + '"\n')
            #
            try:
                vmcn=azr[i]["properties"]["osProfile"]["computerName"]
                vmadmin=azr[i]["properties"]["osProfile"]["adminUsername"]
                fr.write('os_profile {\n')
                fr.write('\tcomputer_name = "' +    vmcn + '"\n')
                fr.write('\tadmin_username = "' +    vmadmin + '"\n')
          
                try : 
                    vmadminpw=azr[i]["properties"]["osProfile"]["Password"]
                    fr.write('\t admin_password = "' +  vmadminpw + '"\n')
                except KeyError:
                    pass

                #  admin_password ?
                fr.write('}\n')
            except KeyError:
                pass 
        
            #
           
            try:
                vmimid=azr[i]["properties"]["storageProfile"]["imageReference"]["id"]  
                #print "do something with "+vmimid
            except KeyError:
                try:
                    vmimpublisher=azr[i]["properties"]["storageProfile"]["imageReference"]["publisher"]
                    vmimoffer=azr[i]["properties"]["storageProfile"]["imageReference"]["offer"]
                    vmimpublisher=azr[i]["properties"]["storageProfile"]["imageReference"]["publisher"]
                    vmimsku=azr[i]["properties"]["storageProfile"]["imageReference"]["sku"]
                    vmimversion=azr[i]["properties"]["storageProfile"]["imageReference"]["version"]
                    fr.write('storage_image_reference {\n')
                    fr.write('\t publisher = "' +  vmimpublisher  + '"\n')
                    fr.write('\t offer = "' +   vmimoffer + '"\n')
                    fr.write('\t sku = "' +   vmimsku + '"\n')
                    fr.write('\t version = "' +   vmimversion + '"\n')
                    havesir=1
                    fr.write('}\n')
                except KeyError:
                    pass
       
            
        
            try :
                vmplname=azr[i]["plan"]["name"]
                vmplprod=azr[i]["plan"]["product"]
                vmplpub=azr[i]["plan"]["publisher"] 
                fr.write('plan {\n')
                fr.write('\t name = "' +  vmplname  + '"\n')
                fr.write('\t publisher = "' +  vmplpub  + '"\n')
                fr.write('\t product = "' +  vmplprod  + '"\n')
                fr.write('}\n')
            except KeyError:
                pass
            #
            #
            #
            try :
                vmdiags=azr[i]["properties"]["diagnosticsProfile"]
                vmbturi=azr[i]["properties"]["diagnosticsProfile"]["bootDiagnostics"]["storageUri"]
                fr.write('boot_diagnostics {\n')
                fr.write('\t enabled = true \n')
                fr.write('\t storage_uri = "' +  vmbturi + '"\n')
                fr.write('}\n')
            except KeyError:
                pass
            #
            if vmtype == "Windows" :
                try:
                    vmwvma=azr[i]["properties"]["osProfile"]["windowsConfiguration"]["provisionVMAgent"]
                    try :
                        vmwau=azr[i]["properties"]["osProfile"]["windowsConfiguration"]["enableAutomaticUpdates"]
                        fr.write('os_profile_windows_config {\n')
                        fr.write('\t enable_automatic_upgrades = ' +  str(vmwau).lower() + '\n')
                        fr.write('\t provision_vm_agent = ' +  str(vmwvma).lower() + '\n')
                        try :
                            vmwtim=azr[i]["properties"]["osProfile"]["windowsConfiguration"]["timeZone"]
                            fr.write('\t timezone =   "' + vmwtim + '"\n')
                        except KeyError:
                            pass
                        fr.write('}\n')
                    except KeyError:
                        pass
                except KeyError:
                    pass
        
            #
            if  vmtype == "Linux" :
                fr.write('os_profile_linux_config {\n')
                try:
                    vmdispw=azr[i]["properties"]["osProfile"]["linuxConfiguration"]["disablePasswordAuthentication"]
                except KeyError:
                    vmdispw="false"
            
                fr.write('\tdisable_password_authentication = ' +  str(vmdispw).lower() + '\n')
                if vmdispw :
                    try:
                        vmsshpath=azr[i]["properties"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["path"]
                        vmsshkey=azr[i]["properties"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["keyData"]
                        t1=str(vmsshkey).rstrip()
                        fr.write('\tssh_keys {\n')
                        fr.write('\t\tpath = "' +   vmsshpath + '"\n')
                        if "----"  not in vmsshkey:
                            fr.write('\t\tkey_data = "' + t1 + '"\n') 
                        else:
                             fr.write('\t\tkey_data = "' + '"\n')
                        fr.write('\t}\n')
                    except KeyError:
                        pass
            
                
                fr.write('}\n')
        

            #
            # OS Disk
            #
            try:
                vmosdiskname=azr[i]["properties"]["storageProfile"]["osDisk"]["name"]
                vmosdiskcache=azr[i]["properties"]["storageProfile"]["osDisk"]["caching"]
                vmoscreoption=azr[i]["properties"]["storageProfile"]["osDisk"]["createOption"]
                fr.write('storage_os_disk {\n')
                fr.write('\t\tname = "' +    vmosdiskname + '"\n')
                fr.write('\t\tcaching = "' +   vmosdiskcache  + '"\n')
                fr.write('\t\tcreate_option = "' + vmoscreoption + '"\n')
                fr.write('\t\tos_type = "' +   vmtype + '"\n')

        
                try :
                    vmossiz=azr[i]["properties"]["storageProfile"]["osDisk"]["diskSizeGB"]
                    fr.write('\t\t disk_size_gb = "' +   str(vmossiz) + '"\n')
                except KeyError:
                    pass   

                try :
                    vmosvhd=azr[i]["properties"]["storageProfile"]["osDisk"]["vhd"]["uri"]
                    fr.write('\t\tvhd_uri = "' +   vmosvhd + '"\n')
                except KeyError:
                    pass
                try :
                    vmoswa=azr[i]["properties"]["storageProfile"]["osDisk"]["writeAcceleratorEnabled"]
                    fr.write('\t write_accelerator_enabled = ' +   str(vmoswa).lower() + '\n')
                except KeyError:
                    pass

                
                if vmoscreoption == "Attach" :
                    try :
                        vmosmdtyp=azr[i]["properties"]["storageProfile"]["osDisk"]["managedDisk"]["storageAccountType"]
                        fr.write('\tmanaged_disk_type = "' +   vmosmdtyp + '"\n')
                    except KeyError:
                        pass
                    try :
                        vmosmdid=azr[i]["properties"]["storageProfile"]["osDisk"]["managedDisk"]["id"]
                        fr.write('\tmanaged_disk_id = "' +   vmosmdid + '"\n')
                    except KeyError:
                        pass
            

                fr.write('}\n')
            except KeyError:
                pass
            #if vmosmdid" try :
            #    if [ havesir -eq 0 :
                    #fr.write('storage_image_reference {'}'  + '"\n')
            #   
            #fi

            #
            # Data disks
            #
            #echo datadisks | jq .
            dcount= len(datadisks)
            
            for j in range(0,dcount):             
                try :
                    ddname= datadisks[j]["name"]
                    ddcreopt= datadisks[j]["createOption"]
                    ddlun= datadisks[j]["lun"]
                    ddvhd= datadisks[j]["vhd.uri"]
                    ddmd= datadisks[j]["managedDisk"]
                    fr.write('storage_data_disk {\n')
                    fr.write('\t name = "' +  ddname + '"\n')
                    fr.write('\t create_option = "' +  ddcreopt + '"\n')
                    fr.write('\t lun = "' +  ddlun + '"\n')
                    # caching , disk_size_gn, write_accelerator_enabled 
                    
                    if ddcreopt == "Attach" :
                        try:
                            ddmdid= datadisks[j]["managedDisk"]["id"].split("/")[8].replace(".","-")
                            ddmdrg= datadisks[j]["managedDisk"]["id"].split("/")[4].replace(".","-").lower()
                            ## ddmdrg  from cut is upper case - not good
                            ## probably safe to assume managed disk in same RG as VM ??
                            # check id lowercase rg = ddmdrg if so use rg
                            #
                            #if not will have to get from terraform state - convert ddmdrg to lc and terraform state output
                            #
                            
                            fr.write('\t managed_disk_id = "${azurerm_managed_disk.' + rg + '__' + ddmdid + '.id} \n')
                        except KeyError:
                            pass
                
                    try :
                        ddvhd= datadisks[j]["vhd"]["uri"]
                        fr.write('\t vhd_uri = "' +  ddvhd + '"\n')
                    except KeyError:
                            pass
                    
                    fr.write('}\n')
                except KeyError:
                    pass
        

            try:
                zones=azr[i]["zones"]
                fr.write('zones = ')
                fr.write(json.dumps(zones, indent=4, separators=(',', ': ')))
                fr.write('\n')
              
            except KeyError:
                pass


    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    tval=tval.replace('"',"'")
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_virtual_machine_extension
#
# azurerm_virtual_machine
def azurerm_virtual_machine_extension(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_virtual_machine_extension"
    tcode="291-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/virtualMachines"
        params = {'api-version': '2019-03-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4].lower()
            try:
                res=azr[i]["resources"]
                rname=name.replace(".","-")
                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for        
                #
                icount=len(res)

            
                if icount > 0 :
                    
                    for j in range(0,icount):
                
                        url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups/" + rg + "/providers/Microsoft.Compute/virtualMachines/"+name+"/extensions"
                    
                        params = {'api-version': '2019-03-01'}
                        r2 = requests.get(url, headers=headers, params=params)
                        azr2= r2.json()["value"]
                        if cde:
                            print(json.dumps(azr2[j], indent=4, separators=(',', ': ')))
                        ename=azr2[j]["name"]
                        ername=ename.replace(".","-")
                        id=azr2[j]["id"]
                        prefix=tfp+"."+rg+'__'+ rname +'__'+ ername
                        #print prefix
                        rfilename=prefix+".tf"
                        fr=open(rfilename, 'w')
                        fr.write(az2tfmess)
                        ename=azr2[j]["name"]
                        thv=azr2[j]["properties"]["typeHandlerVersion"]
                        pub=azr2[j]["properties"]["publisher"]
                        typ=azr2[j]["properties"]["type"]
                        auv=azr2[j]["properties"]["autoUpgradeMinorVersion"]


                        fr.write('resource ' + tfp + ' ' + rg + '__' + rname + '__'+ername +'{\n')
                        fr.write('\t name = "' + ename + '"\n')
                        fr.write('\t location = "'+ loc + '"\n')
                        fr.write('\t resource_group_name = "'+ rgs + '"\n')
                        fr.write('\t publisher = "'+ pub + '"\n')
                        fr.write('\t type_handler_version = "'+ thv + '"\n')
                        fr.write('\t virtual_machine_name = "'+ name + '"\n')
                        fr.write('\t type = "'+ typ + '"\n')
                        fr.write('\t auto_upgrade_minor_version = '+ str(auv).lower() + '\n')


                        try:
                            set=azr2[j]["properties"]["settings"]
                            slen=len(str(set))
                            
                            if slen > 2:
                                fr.write('settings = jsonencode( \n') 
                                fr.write(json.dumps(azr2[j]["properties"]["settings"]))
                                fr.write(')\n') 
                        except KeyError:
                            pass

        # tags block       
                        try:
                            mtags=azr2[j]["tags"]
                            fr.write('tags = { \n')
                            for key in mtags.keys():
                                tval=mtags[key]
                                tval=tval.replace('"',"'")
                                fr.write(('\t "' + key + '"="' + tval + '"\n'))
                            fr.write('}\n')
                        except KeyError:
                            pass

                        fr.write('}\n') 
                        fr.close()   # close .tf file

                        if cde:
                            with open(rfilename) as f: 
                                print (f.read())

                        tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname +'__'+ername + '\n')

                        tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                        
                        tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+'__'+ername+' '+id+'\n'
                        tfim.write(tfcomm)  
            except KeyError:
                pass

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_virtual_machine_scale_set
#
# azurerm_virtual_machine_scale_set
import ast
def azurerm_virtual_machine_scale_set(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp = "azurerm_virtual_machine_scale_set"
    tcode = "295-"
    azr = ""
    if crf in tfp:
        # REST or cli
       
        url = "https://" + cldurl + "/subscriptions/" + sub + \
            "/providers/Microsoft.Compute/virtualMachineScaleSets"
        params = {'api-version': '2019-03-01'}
        r = requests.get(url, headers=headers, params=params)
        azr = r.json()["value"]


        tfrmf = tcode+tfp+"-staterm.sh"
        tfimf = tcode+tfp+"-stateimp.sh"
        tfrm = open(tfrmf, 'a')
        tfim = open(tfimf, 'a')
        print ("# " + tfp,)
        count = len(azr)
        print (count)
        for i in range(0, count):

            name = azr[i]["name"]
            loc = azr[i]["location"]
            id = azr[i]["id"]
            rg = id.split("/")[4].replace(".", "-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))

            rname = name.replace(".", "-")
            prefix = tfp+"."+rg+'__'+rname
            #print prefix
            rfilename = prefix+".tf"
            fr = open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "' + loc + '"\n')
            fr.write('\t resource_group_name = "' + rgs + '"\n')

    ###############
    # specific code start
    ###############

            upm = azr[i]["properties"]["upgradePolicy"]["mode"]
            op = azr[i]["properties"]["overprovision"]
            spg = azr[i]["properties"]["singlePlacementGroup"]
            # vmlic=azr[i]["properties"]["virtualMachineProfile"]["licenseType"]
            # vmpri=azr[i]["properties"]["virtualMachineProfile"]["priority"]

            # vmtype=azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["osDisk"]["osType"]
            #datadisks = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["dataDisks"]


            #vmoswa = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["osDisk"]["writeAcceleratorEnabled"]
            #
            osvhd = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["keyData"]
            #
            #vmimid = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["imageReference"]["id"]


            #

            #vmdispw = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]["disablePasswordAuthentication"]
            #vmsshpath = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["path"]
            #vmsshkey = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["keyData"]
            #
  
            #

    # sku block
            skun = azr[i]["sku"]["name"]
            skuc = azr[i]["sku"]["capacity"]
            skut = azr[i]["sku"]["tier"]
            fr.write('sku { \n')
            fr.write('\tname = "' + skun + '"\n')
            fr.write('\ttier = "' + skut + '"\n')
            fr.write('\tcapacity = "' + str(skuc) + '"\n')
            fr.write('} \n')
    # basic settings continued

            try:
                vmlic = azr[i]["properties"]["virtualMachineProfile"]["licenseType"]
                fr.write('license_type = "' + vmlic + '"\n')
            except KeyError:
                pass

            fr.write('upgrade_policy_mode = "' + upm + '"\n')
            fr.write('overprovision = ' + str(op).lower() + '\n')
            fr.write('single_placement_group = ' + str(spg).lower() + '\n')
            try:
                vmpri = azr[i]["properties"]["virtualMachineProfile"]["priority"]
                fr.write('priority = "' + vmpri + '"\n')
            except KeyError:
                pass

    # os_profile block
            vmadmin = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["adminUsername"]
            vmcn = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["computerNamePrefix"]
            fr.write('os_profile { \n')
            fr.write('\tcomputer_name_prefix = "' + vmcn + '"\n')
            fr.write('\tadmin_username = "' + vmadmin + '"\n')
            try:
                vmadminpw = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["Password"]
                fr.write('\tadmin_password = "' + vmadminpw + '"\n')
            except KeyError:
                pass

            fr.write('}\n')

    # os_profile_secrets - not used ?

    # os_profile_windows_config
            try:  # winb
                winb = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]
                vmwau = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]["enableAutomaticUpdates"]
                vmwvma = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]["provisionVmAgent"]
                vmwtim = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]["timeZone"]
                try:
                    vmwau = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]["enableAutomaticUpdates"]
                    fr.write('os_profile_windows_config {\n')
                    fr.write('\t enable_automatic_upgrades = ' + str(vmwau).lower() + '\n')
                    fr.write('\t provision_vm_agent = ' + str(vmwvma).lower() + '\n')
                    try:
                        vmwtim = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]["timeZone"]
                        fr.write('\t timezone =   "' + vmwtim + '"\n')
                    except KeyError:
                        pass
                    fr.write('}\n')
                except KeyError:
                    pass
            except KeyError:
                pass

    # os_profile_linux_config block


            try:  # linuxb" try :
                linuxb = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]
                vmdispw = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]["disablePasswordAuthentication"]
                vmsshpath = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["path"]
                vmsshkey = azr[i]["properties"]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["keyData"]
                fr.write('os_profile_linux_config {\n')
                if vmdispw == "null":
                    # osprofile can by null for vhd imported images - must make an artificial one.
                    vmdispw = "false"

                fr.write('\tdisable_password_authentication = ' + str(vmdispw).lower() + '\n')
                if vmdispw != "false":
                    fr.write('\tssh_keys { \n')
                    fr.write('\t\tpath = "' + vmsshpath + '"\n')
                    fr.write('\t\tkey_data = "' +   vmsshkey.rstrip() + '"\n') 
                    fr.write('\t}\n')

                fr.write('}\n')
            except KeyError:
                pass


# network profile block
            netifs = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"]
            icount = len(netifs)
            if icount > 0:
                for j in range(0, icount):
                    fr.write('network_profile { \n')

                    nn = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["name"]
                    fr.write('\tname = "' + nn + '"\n')
                    ipc = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["properties"]["ipConfigurations"]
                                       
                    try:
                        pri = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["properties"]["primary"]
                        fr.write('\tprimary = ' + str(pri).lower() + '\n')
                    except KeyError:
                        pass
                    
                    kcount = len(ipc)
                    if kcount > 0:
                        for k in range(0, kcount):
                            fr.write('\tip_configuration { \n')
                            ipcn = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["properties"]["ipConfigurations"][k]["name"]

                            ipcsrg = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["properties"]["ipConfigurations"][k]["properties"]["subnet"]["id"].split("/")[4].replace(".", "-").lower()
                            ipcsn = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["properties"]["ipConfigurations"][k]["properties"]["subnet"]["id"].split("/")[10].replace(".", "-")
                            beapids = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["properties"]["ipConfigurations"][k]["properties"]["loadBalancerBackendAddressPools"]
                            #natrids = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["properties"]["ipConfigurations"][k]["properties"]["loadBalancerInboundNatPools"]

                            fr.write('\t\tname = "' + ipcn + '"\n')
                            try:
                                ipcp = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["properties"]["ipConfigurations"][k]["primary"]
                                fr.write('\t\tprimary = "' + ipcp + '"\n')
                            except KeyError:
                                fr.write('\t\tprimary = true\n')
                            
                            try:
                                ipcsrg = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["properties"]["ipConfigurations"][k]["properties"]["subnet"]["id"].split("/")[4].replace(".", "-").lower()
                                ipcsn = azr[i]["properties"]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["properties"]["ipConfigurations"][k]["properties"]["subnet"]["id"].split("/")[10].replace(".", "-")
                                if ipcsrg[0].isdigit(): ipcsrg="rg_"+ipcsrg
                                fr.write('\t\tsubnet_id = "${azurerm_subnet.' + ipcsrg + '__' + ipcsn + '.id}"\n')
                            except KeyError:
                                pass
                            fr.write('\t}\n')

                    fr.write('}\n')

    # storage_profile_os_disk  block
            try:
                vmosdiskname = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["osDisk"]["name"]
                vmosdiskcache = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["osDisk"]["caching"]
                vmoscreoption = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["osDisk"]["createOption"]

                fr.write('storage_profile_os_disk {\n')
                fr.write('\tname = "' + vmosdiskname + '"\n')
                fr.write('\tcaching = "' + vmosdiskcache + '"\n')
                # look at this
                # if vmosacctype != "" :
                ##    fr.write('\tmanaged_disk_type = "' +   vmosacctype + '"\n')

                fr.write('\tcreate_option = "' + vmoscreoption + '"\n')

                try:
                    vmtype = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["osDisk"]["osType"]
                except KeyError:
                    vmtype = ""
                    pass
                fr.write('\tos_type = "' + vmtype + '"\n')

                try:
                    vmoswa = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["osDisk"]["writeAcceleratorEnabled"]
                    fr.write('\t write_accelerator_enabled = ' + str(vmoswa).lower() + '\n')
                except KeyError:
                    pass


                try:
                    vmosvhdc = str(ast.literal_eval(json.dumps(azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["osDisk"]["vhdContainers"])))
                    vmosvhdc=vmosvhdc.replace("'",'"')
                    fr.write('\tvhd_containers = ' + vmosvhdc + '\n')
                except KeyError:
                    pass

                fr.write('}\n')
                #
            except KeyError:
                pass

    # storage_profile_data_disk  block

    
            try:
                datadisks = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["dataDisks"]
                dcount = len(datadisks)
                for j in range(0, dcount):

                    ddname = datadisks["name"]
                    ddcreopt = datadisks["createOption"]
                    ddlun = datadisks[j]["lun"]
                    ddvhd = datadisks[j]["vhd"]["uri"]
                    ddmd = datadisks[j]["managedDisk"]
                    fr.write('storage_profile_data_disk { \n')
                    fr.write('\t name = "' + ddname + '"\n')
                    fr.write('\t create_option = "' + ddcreopt + '"\n')
                    fr.write('\t lun = "' + ddlun + '"\n')
                    # caching , disk_size_gn, write_accelerator_enabled

                    if ddcreopt == "Attach":
                        try:
                            ddmd = datadisks[j]["managedDisk"]
                            ddmdid = datadisks[j]["managedDisk"]["id"].split(
                                "/")[8].replace(".", "-")
                            ddmdrg = datadisks[j]["managedDisk"]["id"].split("/")[4].replace(".", "-").lower()
                            # ddmdrg from cut is upper case - not good
                            # probably safe to assume managed disk in same RG as VM ??
                            # check id lowercase rg = ddmdrg if so use rg
                            #
                            # if not will have to get from terraform state - convert ddmdrg to lc and terraform state output
                            #

                            fr.write(
                                '\t managed_disk_id = "${azurerm_managed_disk.' + rg + '__' + ddmdid + '.id}"\n')
                        except KeyError:
                            pass

                    try:
                        ddvhd = datadisks[j]["vhd"]["uri"]
                        fr.write('\t vhd_uri = "' + ddvhd + '"\n')
                    except KeyError:
                        pass

                    fr.write('}\n')

                # end for j
            except KeyError:
                pass

    # storage_profile_image_reference block
            try:
                vmimid = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["imageReference"]["id"]
                #print "do something with image id" + vmimid
            except KeyError:
                try:
                    vmimpublisher = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["imageReference"]["publisher"]
                    vmimoffer = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["imageReference"]["offer"]
                    vmimpublisher = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["imageReference"]["publisher"]
                    vmimsku = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["imageReference"]["sku"]
                    vmimversion = azr[i]["properties"]["virtualMachineProfile"]["storageProfile"]["imageReference"]["version"]
                    fr.write('storage_profile_image_reference { \n')
                    fr.write('\t publisher = "' + vmimpublisher + '"\n')
                    fr.write('\t offer = "' + vmimoffer + '"\n')
                    fr.write('\t sku = "' + vmimsku + '"\n')
                    fr.write('\t version = "' + vmimversion + '"\n')

                    fr.write('}\n')
                except KeyError:
                    pass
                pass
        

    # extensions:
            try:
                vmexts = azr[i]["properties"]["virtualMachineProfile"]["extensionProfile"]["extensions"]
                dcount = len(vmexts)
                for j in range(0, dcount):
                    vmextn=azr[i]["properties"]["virtualMachineProfile"]["extensionProfile"]["extensions"][j]["name"]
                    fr.write('extension {\n')
                    fr.write('\t name = "' + vmextn + '"\n')
                    vmextpub=azr[i]["properties"]["virtualMachineProfile"]["extensionProfile"]["extensions"][j]["properties"]["publisher"]
                    vmexttyp=azr[i]["properties"]["virtualMachineProfile"]["extensionProfile"]["extensions"][j]["properties"]["type"]
                    vmextthv=azr[i]["properties"]["virtualMachineProfile"]["extensionProfile"]["extensions"][j]["properties"]["typeHandlerVersion"]
                    
                    fr.write('\t publisher = "' + vmextpub + '"\n')
                    fr.write('\t type = "' + vmexttyp + '"\n')
                    fr.write('\t type_handler_version = "' + vmextthv + '"\n')
                    fr.write('\t protected_settings = ""\n')    
                    
                    try:
                        vmextset=str(ast.literal_eval(json.dumps(azr[i]["properties"]["virtualMachineProfile"]["extensionProfile"]["extensions"][j]["properties"]["settings"])))
                        vmextset=vmextset.replace("'",'\\"')
                        #print "vmextsett=" + vmextset
                    
                        fr.write('\t settings="' + vmextset + '"\n')                           

                    except KeyError:
                        pass
                    
                    fr.write('}\n')
            except KeyError:
                pass



    # boot diagnostics block

            try:
                vmbten = azr[i]["properties"]["virtualMachineProfile"]["diagnosticsProfile"]["bootDiagnostics"]["enabled"]
                vmbturi = azr[i]["properties"]["virtualMachineProfile"]["diagnosticsProfile"]["bootDiagnostics"]["storageUri"]
                fr.write('boot_diagnostics {\n')
                fr.write('\t enabled = ' + str(vmbten).lower() + '\n')
                fr.write('\t storage_uri = "' + vmbturi + '"\n')
                fr.write('}\n')
            except KeyError:
                pass

    # plan block
            try:
                vmplname = azr[i]["plan"]["name"]
                vmplprod = azr[i]["plan"]["product"]
                vmplpub = azr[i]["plan"]["publisher"]
                fr.write('plan {\n')
                fr.write('\t name = "' + vmplname + '"\n')
                fr.write('\t publisher = "' + vmplpub + '"\n')
                fr.write('\t product = "' + vmplprod + '"\n')
                fr.write('}\n')
            except KeyError:
                pass

    # zones block

            try:
                zones=azr[i]["zones"]
                fr.write('zones = ')
                fr.write(json.dumps(zones, indent=4, separators=(',', ': ')))
                fr.write('\n')
            except KeyError:
                pass

    # tags block
            try:
                mtags = azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval = mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n')
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f:
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) +
                       ' of ' + str(count-1) + '"' + '\n')
            tfcomm = 'terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)

        # end for i loop

        tfrm.close()
        tfim.close()
    # end stub

 
#
# azurerm_automation_account
#
# azurerm_automation_account
def azurerm_automation_account(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_automation_account"
    tcode="310-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Automation/automationAccounts"
        params = {'api-version': '2018-06-30'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            try:
                #sku=azr[i]["properties"]["sku"]["name"]
                #if sku == "Free" :
                #    sku="Basic"
                sku="Basic"

                
                fr.write('\t sku_name = "' + sku + '"\n')
             
            except KeyError:
                pass

    # tags block       
            try:
                mtags=azr[i]["tags"]          
                if mtags is not None:
                    fr.write('tags = { \n')
                    for key in mtags.keys():
                        tval=mtags[key]
                        fr.write(('\t "' + key + '"="' + tval + '"\n'))
                    fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_log_analytics_workspace
#
# azurerm_log_analytics_workspace
def azurerm_log_analytics_workspace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_log_analytics_workspace"
    tcode="320-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.OperationalInsights/workspaces"
        params = {'api-version': '2015-03-20'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')


            sku=azr[i]["properties"]["sku"]["name"]
            rdays=azr[i]["properties"]["retentionInDays"]

            fr.write('\t sku =   "'+sku + '"\n')
            # 7 is not a valid value, but is the default reported from AZ api. If 7, skip to avoid triggering plan difference
            if str(rdays) != "7" :
                fr.write('\t retention_in_days = "'+str(rdays) + '"\n')
   

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_log_analytics_solution
#
# azurerm_log_analytics_solution
def azurerm_log_analytics_solution(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_log_analytics_solution"
    tcode="330-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST solutions"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.OperationsManagement/solutions"
        params = {'api-version': '2015-11-01-preview'}
        #2015-11-01-preview
        r = requests.get(url, headers=headers, params=params)
        
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            skip="false"
            #print id
            if "[" in id or "]" in id :
                print ("Skipping this soluion "+ name+ " can't process currently")
                skip="true"
                return


            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            rname=rname.replace("(","-")  #| sed s/\(/-/
            rname=rname.replace(")","-") # | sed s/\)/-/

            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            #fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            pname= name
            name= name.replace("(","-")  #| sed s/\(/-/
            name= name.replace(")","-") # | sed s/\)/-/
   

           
            pub=azr[i]["plan"]["publisher"]
            prod=azr[i]["plan"]["product"]
            soln=azr[i]["plan"]["product"].split("/")[1]
            workname=azr[i]["properties"]["workspaceResourceId"].split("/")[8]
            workn1=azr[i]["name"].split("(")[1]
            workn= workn1.split(")")[0]
            workid=azr[i]["properties"]["workspaceResourceId"]
            
            if skip != "true" :
                
                fr.write('\t solution_name = "' +  soln + '"\n')
                fr.write('\t workspace_name = "' +  workn + '"\n')
                fr.write('\t workspace_resource_id = "' +  workid + '"\n')
                
                fr.write('\t plan {\n')
                fr.write('\t\t publisher =  "'+pub + '"\n')
                fr.write('\t\t product = "' + prod + '"\n')
                fr.write('\t }\n')

# tags cause errors                
                

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' "'+id+'"\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_image
#
# azurerm_image
def azurerm_image(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_image"
    tcode="340-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/images"
        params = {'api-version': '2019-03-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')
             
# hardwire this - as source vm may of been deleted after image created
            try:
                svm=azr[i]["properties"]["sourceVirtualMachine"]["id"]
                fr.write('\t source_virtual_machine_id = "' +  svm + '"\n')
            except KeyError:        
                try :
                    osdisk=azr[i]["properties"]["storageProfile"]["osDisk"]
                    ostype=azr[i]["properties"]["storageProfile"]["osDisk"]["osType"]
                    osstate=azr[i]["properties"]["storageProfile"]["osDisk"]["osState"]
                    oscache=azr[i]["properties"]["storageProfile"]["osDisk"]["caching"]

                    fr.write('\t os_disk {\n')
                    fr.write('\t os_type = "' +  ostype + '"\n')
                    fr.write('\t os_state = "' +  osstate + '"\n')
                    fr.write('\t caching = "' +  oscache + '"\n')
                    
                    try :
                        blob_uri=azr[i]["properties"]["storageProfile"]["osDisk"]["blobUri"]
                        fr.write('\t blob_uri = "' +  blob_uri + '"\n')
                    except KeyError:
                        pass
                    fr.write('\t}\n')
            
                except KeyError:
                    pass
                    
                pass

            try:
                zros=azr[i]["properties"]["storageProfile"]["zoneResilient"]
                fr.write('\t zone_resilient = '+ str(zros).lower() + '\n')
            except KeyError:
                pass

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_shared_image_gallery
#
# azurerm_snapshot
def azurerm_shared_image_gallery(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_shared_image_gallery"
    tcode="341-"
    azr=""
    #cde=False
    if crf in tfp:
    # REST or cli
        # print "REST snapshot"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/galleries"
        params = {'api-version': '2019-03-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')


            try:
                co=azr[i]["properties"]["description"]
                fr.write('\t description = "' +  co + '"\n')
            except KeyError:
                pass




    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_shared_image
#
# azurerm_snapshot
def azurerm_shared_image(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_shared_image"
    tcode="342-"
    azr=""
    #cde=False
    if crf in tfp:
    # REST or cli
        # print "REST snapshot"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/galleries"
        params = {'api-version': '2019-03-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

    
        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        
        count=len(azr)
        for i in range(0, count):

            gname=azr[i]["name"]
            gloc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4].lower()
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
        


            url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups/"+rg+"/providers/Microsoft.Compute/galleries/"+gname+"/images"
            params = {'api-version': '2019-03-01'}
            r = requests.get(url, headers=headers, params=params)
            azr2= r.json()["value"]
            jcount=len(azr2)
            print ("# " + tfp,)
            print (jcount)
            for j in range(0, jcount):
                
                if cde:
                    print(json.dumps(azr2[j], indent=4, separators=(',', ': ')))
                name=azr2[j]["name"]
                loc=azr2[j]["location"]
                id=azr2[j]["id"]

                rname=name.replace(".","-")
                
                prefix=tfp+"."+rg+'__'+gname+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + gname + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t location = "'+ loc + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')
                fr.write('\t gallery_name = "'+ gname + '"\n')

                try:
                    ost=azr2[j]["properties"]["osType"]
                    fr.write('\t os_type = "' +  ost + '"\n')
                except KeyError:
                    pass
                sku=azr2[j]["properties"]["identifier"]["sku"]
                pub=azr2[j]["properties"]["identifier"]["publisher"]
                off=azr2[j]["properties"]["identifier"]["offer"]
                fr.write('\t identifier { \n')
                fr.write('\t\t sku ="'+sku+'"\n')
                fr.write('\t\t publisher ="'+pub+'"\n')
                fr.write('\t\t offer ="'+off+'"\n')
                fr.write('\t} \n')


        # tags block       
                try:
                    mtags=azr2[j]["tags"]
                    fr.write('tags = { \n')
                    for key in mtags.keys():
                        tval=mtags[key]
                        fr.write(('\t "' + key + '"="' + tval + '"\n'))
                    fr.write('}\n')
                except KeyError:
                    pass

                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+gname+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(j) + ' of ' + str(jcount-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+gname+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_shared_image_version
#
# azurerm_snapshot
def azurerm_shared_image_version(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_shared_image_version"
    tcode="343-"
    azr=""
    #cde=False
    if crf in tfp:
    # REST or cli
        # print "REST snapshot"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/galleries"
        params = {'api-version': '2019-03-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

    
        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        
        count=len(azr)
  
        for i in range(0, count):

            gname=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
        
            url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups/"+rg+"/providers/Microsoft.Compute/galleries/"+gname+"/images"
            params = {'api-version': '2019-03-01'}
            r = requests.get(url, headers=headers, params=params)
            azr2= r.json()["value"]
            jcount=len(azr2)
           
            for j in range(0, jcount):

                iname=azr2[j]["name"]
                rname=iname.replace(".","-")

                url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups/"+rg+"/providers/Microsoft.Compute/galleries/"+gname+"/images/"+iname+"/versions"
                params = {'api-version': '2019-03-01'}
                r = requests.get(url, headers=headers, params=params)
                azr3= r.json()["value"]
                kcount=len(azr3)
                print ("# " + tfp,)
                print (kcount)
                for k in range(0, kcount):

                    if cde:
                        
                        print(json.dumps(azr3[k], indent=4, separators=(',', ': ')))

                    name=azr3[k]["name"]
                    loc=azr3[k]["location"]
                    id=azr3[k]["id"]
                    rg=id.split("/")[4].replace(".","-").lower()
                    if rg[0].isdigit(): rg="rg_"+rg
                    rgs=id.split("/")[4]
                    rname = name.replace(".", "-")
                    riname=iname.replace(".", "-")
                    prefix=tfp+"."+rg+'__'+gname+'__'+riname+'__'+rname
                    
                    #print prefix
                    rfilename=prefix+".tf"
                    fr=open(rfilename, 'w')
                    fr.write(az2tfmess)
                  
                    fr.write('resource ' + tfp + ' ' + rg + '__' + gname + '__' + riname + '__' + rname + ' {\n')  
                    fr.write('\t name = "' + name + '"\n')
                    fr.write('\t location = "'+ loc + '"\n')
                    fr.write('\t resource_group_name = "'+ rgs + '"\n')
                    fr.write('\t gallery_name = "'+ gname + '"\n')
                    fr.write('\t image_name = "'+ iname + '"\n')
                    mid=azr3[k]["properties"]["publishingProfile"]["source"]["managedImage"]["id"]  
                    fr.write('\t managed_image_id = "'+ mid + '"\n')
                    try:
                        tr=azr3[k]["properties"]["publishingProfile"]["targetRegions"]
                        tcount=len(tr)
                        
                        for t in range(0, tcount):
                            tnam=tr[t]["name"]
                            rrc=tr[t]["regionalReplicaCount"]
                            fr.write('\t target_region { \n')
                            fr.write('\t\t name ="'+tnam+'"\n') 
                            fr.write('\t\t regional_replica_count ="'+str(rrc)+'"\n')  
                            fr.write('\t} \n')



                    except KeyError:
                        pass



            # tags block       
                    try:
                        mtags=azr3[k]["tags"]
                        fr.write('tags = { \n')
                        for key in mtags.keys():
                            tval=mtags[key]
                            fr.write(('\t "' + key + '"="' + tval + '"\n'))
                        fr.write('}\n')
                    except KeyError:
                        pass

                    fr.write('}\n') 
                    fr.close()   # close .tf file

                    if cde:
                        with open(rfilename) as f: 
                            print (f.read())

                   
                    tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+gname+'__'+riname+'__'+rname + '\n')
                    tfim.write('echo "importing ' + str(k) + ' of ' + str(kcount-1) + '"' + '\n')
                    tfcomm='terraform import '+tfp+'.'+rg+'__'+gname+'__'+riname+'__'+rname+' '+id+'\n'
                  
                    tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_snapshot
#
# azurerm_snapshot
def azurerm_snapshot(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_snapshot"
    tcode="350-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST snapshot"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/snapshots"
        params = {'api-version': '2018-09-30'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')



            #suri=azr[i]["creationData"]["sourceUri"]
            #srid=azr[i]["creationData"]["sourceResourceId"]
            #said=azr[i]["creationData"]["storageAccountId"]
            try:
                co=azr[i]["properties"]["creationData"]["createOption"]
                fr.write('\t create_option = "' +  co + '"\n')
            except KeyError:
                pass


            try :
                sz=azr[i]["properties"]["diskSizeGb"]
                fr.write('\t disk_size_gb = "' +  sz + '"\n')
       
            #if suri" try :
            #    fr.write('\t source_uri = "' +  suri + '"\n')
            #fi
            #if srid" try :
            #    fr.write('\t source_resource_id = "' +  srid + '"\n')
            #fi
            #if said" try :
            #    fr.write('\t source_account_id = "' +  said + '"\n')
            #fi        
            except KeyError:
                pass


    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_network_watcher
#
# azurerm_network_watcher
def azurerm_network_watcher(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_network_watcher"
    tcode="360-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/networkWatchers"
        params = {'api-version': '2019-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')


    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_cosmosdb_account
#
# azurerm_cosmosdb_account
def azurerm_cosmosdb_account(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_cosmosdb_account"
    tcode="400-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.DocumentDB/databaseAccounts"
        params = {'api-version': '2016-03-31'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')


        #azr=az cosmosdb list -g rgsource -o json
  
            kind=azr[i]["kind"]
            offer=azr[i]["properties"]["databaseAccountOfferType"]
            cp=azr[i]["properties"]["consistencyPolicy"]["defaultConsistencyLevel"]
            mis=azr[i]["properties"]["consistencyPolicy"]["maxIntervalInSeconds"]
            msp=azr[i]["properties"]["consistencyPolicy"]["maxStalenessPrefix"] 
            
            geol=azr[i]["properties"]["failoverPolicies"]     
                
            af=azr[i]["properties"]["enableAutomaticFailover"]      
                

            fr.write('\t kind = "' +  kind + '"\n')
            fr.write('\t offer_type = "' +  offer + '"\n')
            fr.write('\t consistency_policy {\n')
            fr.write('\t\t  consistency_level = "' +  cp + '"\n')
            fr.write('\t\t  max_interval_in_seconds = "' +  str(mis) + '"\n')
            fr.write('\t\t  max_staleness_prefix = "' +  str(msp) + '"\n')
            fr.write('\t }\n')
            fr.write('\t enable_automatic_failover = ' +  str(af).lower() + '\n')
        # capabilities block

            # code out terraform error
            try:
                caps=azr[i]["properties"]["capabilities"][0]["name"] 
                if caps == "EnableTable" or caps == "EnableGremlin" or caps == "EnableCassandra":
                    fr.write('\t capabilities {\n')
                    fr.write('\t\t name = "' +  caps + '"\n')        
                    fr.write('\t }\n')
            except KeyError:
                pass
            except IndexError:
                pass
            
        # geo location block
                
            icount= len(geol)
            for j in range(0,icount):
                    floc=azr[i]["properties"]["failoverPolicies"][j]["locationName"]
                    fop=azr[i]["properties"]["failoverPolicies"][j]["failoverPriority"]
                    fr.write('\t geo_location {\n')
                    fr.write('\t location = "'+floc + '"\n')
                    fr.write('\t failover_priority  = "' + str(fop) + '"\n')
                    fr.write('}\n')

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_servicebus_namespace
#
# azurerm_servicebus_namespace
def azurerm_servicebus_namespace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_servicebus_namespace"
    tcode="500-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST SB namespaces"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.ServiceBus/namespaces"
        params = {'api-version': '2017-04-01'}
        r = requests.get(url, headers=headers, params=params)
        try:
            azr= r.json()["value"]
        except KeyError:
            if cde: print ("No Namespace resources found")
            return


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            sku=azr[i]["sku"]["tier"]
               
            fr.write('\t sku = "' +  sku + '"\n')
            try :
                cap=azr[i]["sku"]["capacity"]
                fr.write('\t capacity = "' +  str(cap) + '"\n')
            except KeyError:
                pass

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_servicebus_queue
#
# azurerm_servicebus_queue
def azurerm_servicebus_queue(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_servicebus_queue"
    tcode="510-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST namespace for queue"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.ServiceBus/namespaces"
        params = {'api-version': '2017-04-01'}
        r = requests.get(url, headers=headers, params=params)
        #print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
        try:
            azr= r.json()["value"]
        except KeyError:
            if cde: print ("Found no Namespaces for Queues")
            return

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            nname=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            rgs=id.split("/")[4]
            #print id
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
 
            url="https://management.azure.com/" + id + "/queues"
            params = {'api-version': '2017-04-01'}
            r = requests.get(url, headers=headers, params=params)
            #print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
            try:
                azr2= r.json()["value"]
            except KeyError:
                print ("Found no SB Queues")
                return
            
            if cde:
                print(json.dumps(azr2, indent=4, separators=(',', ': ')))
        

    ###############
    # specific code start
    ###############
        
        
      
        #azr2=az servicebus queue list -g rgsource --namespace-name nname -o json
            icount=len(azr2)
            if icount > 0 :
                for j in range(0,icount):
                    name= azr2[j]["name"]
                    rname= name.replace(".","-")
                    id= azr2[j]["id"]
                    rg=id.split("/")[4].replace(".","-").lower()
                    if rg[0].isdigit(): rg="rg_"+rg
                    rgs=id.split("/")[4]

                    rname=name.replace(".","-")
                    prefix=tfp+"."+rg+'__'+rname
                    #print prefix
                    rfilename=prefix+".tf"
                    fr=open(rfilename, 'w')
                    fr.write(az2tfmess)
                    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                    fr.write('\t name = "' + name + '"\n')
                   
                    fr.write('\t resource_group_name = "'+ rgs + '"\n')


                    ep= azr2[j]["properties"]["enablePartitioning"]
                    adoni= azr2[j]["properties"]["autoDeleteOnIdle"]
                    
                    ee= azr2[j]["properties"]["enableExpress"]
                    dd= azr2[j]["properties"]["requiresDuplicateDetection"]
                    rs= azr2[j]["properties"]["requiresSession"]
                    mx= azr2[j]["properties"]["maxSizeInMegabytes"]
                    dl= azr2[j]["properties"]["deadLetteringOnMessageExpiration"]
                    
                    fr.write('\t namespace_name = "' +  nname + '"\n')
                    fr.write('\t enable_partitioning =  '+str(ep).lower() + '\n')
                    fr.write('\t enable_express =  '+str(ee).lower() + '\n')
                    fr.write('\t requires_duplicate_detection ='+  str(dd).lower() + '\n')
                    fr.write('\t requires_session =  '+ str(rs).lower() + '\n')
                    # tf problem with this one. tf=1k cli=16k
                    #fr.write('\t max_size_in_megabytes =  mx + '"\n')
                    fr.write('\t dead_lettering_on_message_expiration = ' +str(dl).lower() + '\n')
                

        # no tags block       


                    fr.write('}\n') 
                    fr.close()   # close .tf file

                    if cde:
                        with open(rfilename) as f: 
                            print (f.read())

                    tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                    tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                    tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                    tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_eventhub_namespace
#
# azurerm_eventhub
def azurerm_eventhub_namespace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):

    tfp="azurerm_eventhub_namespace"
    tcode="520-"
    azr=""
    
    if crf in tfp:
   
    # REST or cli
        # print "REST SB namespaces"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.EventHub/namespaces"
        params = {'api-version': '2017-04-01'}
        r = requests.get(url, headers=headers, params=params)
        try:
            azr= r.json()["value"]
        except KeyError:
            if cde: print ("No Namespace resources found")
            return
        
        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            sku=azr[i]["sku"]["tier"]
               
            fr.write('\t sku = "' +  sku + '"\n')
            try :
                cap=azr[i]["sku"]["capacity"]
                fr.write('\t capacity = "' +  str(cap) + '"\n')
            except KeyError:
                pass

            kafka=azr[i]["properties"]["kafkaEnabled"]
            maxt=azr[i]["properties"]["maximumThroughputUnits"]
            autoi=azr[i]["properties"]["isAutoInflateEnabled"]

            fr.write('\t auto_inflate_enabled = "' +  str(autoi).lower() + '"\n')
            fr.write('\t maximum_throughput_units = "' +  str(maxt) + '"\n')
            fr.write('\t kafka_enabled = "' +  str(kafka).lower() + '"\n')

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_eventhub
#
# azurerm_servicebus_queue
def azurerm_eventhub(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_eventhub"
    tcode="521-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST namespace for queue"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.EventHub/namespaces"
        params = {'api-version': '2017-04-01'}
        r = requests.get(url, headers=headers, params=params)
        #print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
        try:
            azr= r.json()["value"]
        except KeyError:
            if cde: print ("Found no Namespaces for EventHubs")
            return

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            nname=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            #print id
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
 
            url="https://management.azure.com/" + id + "/eventhubs"
            params = {'api-version': '2017-04-01'}
            r = requests.get(url, headers=headers, params=params)
            #print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
            try:
                azr2= r.json()["value"]
            except KeyError:
                print ("Found no EventHubs")
                return
            
            if cde:
                print ("****")
                print(json.dumps(azr2, indent=4, separators=(',', ': ')))
        

    ###############
    # specific code start
    ###############
        
        
      
        #azr2=az servicebus queue list -g rgsource --namespace-name nname -o json
            icount=len(azr2)
            if icount > 0 :
                for j in range(0,icount):
                    name= azr2[j]["name"]
                    rname= name.replace(".","-")
                    id= azr2[j]["id"]
                    rg=id.split("/")[4].replace(".","-").lower()
                    rgs=id.split("/")[4]

                    rname=name.replace(".","-")
                    prefix=tfp+"."+rg+'__'+rname
                    #print prefix
                    rfilename=prefix+".tf"
                    fr=open(rfilename, 'w')
                    fr.write(az2tfmess)
                    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                    fr.write('\t name = "' + name + '"\n')
                   
                    fr.write('\t resource_group_name = "'+ rgs + '"\n')
                    fr.write('\t namespace_name = "' +  nname + '"\n')

                    pc= azr2[j]["properties"]["partitionCount"]
                    mr= azr2[j]["properties"]["messageRetentionInDays"]
                    
                    
                    fr.write('\t partition_count =  '+str(pc) + '\n')
                    fr.write('\t message_retention =  '+str(mr) + '\n')

                

        # no tags block       


                    fr.write('}\n') 
                    fr.close()   # close .tf file

                    if cde:
                        with open(rfilename) as f: 
                            print (f.read())

                    tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                    tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                    tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                    tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_eventhub_namespace_authorization_rule
#
# azurerm_eventhub_namespace_authorization_rule
def azurerm_eventhub_namespace_authorization_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_eventhub_namespace_authorization_rule"
    tcode="522-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST namespace for queue"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.EventHub/namespaces"
        params = {'api-version': '2017-04-01'}
        r = requests.get(url, headers=headers, params=params)
        #print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
        try:
            azr= r.json()["value"]
        except KeyError:
            if cde: print ("Found no Namespaces for EventHubs")
            return

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            nname=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            rgs=id.split("/")[4]
            #print id
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print ("azr")
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            url="https://management.azure.com/" + id + "/AuthorizationRules"
            params = {'api-version': '2017-04-01'}

            r = requests.get(url, headers=headers, params=params)
            print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
            try:
                azr2= r.json()["value"]
            except KeyError:
                print ("Found no EventHub")
                return
            
            if cde:
                print ("****")
                print(json.dumps(azr2, indent=4, separators=(',', ': ')))
        
            icount=len(azr2)
            for j in range(0, icount):

                name=azr2[j]["name"]
                loc=azr2[j]["location"]
                id=azr2[j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if rg[0].isdigit(): rg="rg_"+rg
                rgs=id.split("/")[4]
                #print id
                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for
                if cde:
                    print(json.dumps(azr2[i], indent=4, separators=(',', ': ')))
            
    ###############
    # specific code start
    ###############
        
                rname= name.replace(".","-")     
                prefix=tfp+"."+rg+'__'+rname
                        #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')               
                fr.write('\t resource_group_name = "'+ rgs + '"\n')
                fr.write('\t namespace_name = "' +  nname + '"\n')


                rights= azr2[j]["properties"]["rights"]
   
                if "Listen" in str(rights):
                    fr.write('\t listen = true\n')
                else:
                    fr.write('\t listen = false\n')

                if "Send" in str(rights):
                    fr.write('\t send = true\n')
                else:
                    fr.write('\t send = false\n')

                if "Manage" in str(rights):
                    fr.write('\t manage = true\n')
                else:
                    fr.write('\t manage = false\n')               

        # no tags block       

                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

 
#
# azurerm_sql_server
#
# azurerm_sql_server
def azurerm_sql_server(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_sql_server"
    tcode="540-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST SQL Servers"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Sql/servers"
        params = {'api-version': '2015-05-01-preview'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            ver=azr[i]["properties"]["version"]
            al=azr[i]["properties"]["administratorLogin"]

            fr.write('\t version = "' +  ver + '"\n')
            fr.write('\t administrator_login= "' +  al + '"\n')
            
            try :
                ap=azr[i]["properties"]["administratorLoginPassword"]
                fr.write('\t administrator_login_password= "' +  ap + '"\n')
            except KeyError:
                fr.write('\t administrator_login_password= ""\n')
                pass

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_sql_database
#
# azurerm_sql_database
def azurerm_sql_database(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp = "azurerm_sql_database"
    tcode = "541-"
    azr = ""
    if crf in tfp:
    # REST or cli
        # print "REST SQL Servers"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Sql/servers"
        params = {'api-version': '2015-05-01-preview'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf = tcode+tfp+"-staterm.sh"
        tfimf = tcode+tfp+"-stateimp.sh"
        tfrm = open(tfrmf, 'a')
        tfim = open(tfimf, 'a')
        print ("# " + tfp,)
        count = len(azr)
        print (count)
        for i in range(0, count):
            
            name = azr[i]["name"]
            loc = azr[i]["location"]
            id = azr[i]["id"]
            rg = id.split("/")[4].replace(".", "-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs = id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))


            sname=name

# azr=az sql db list --server sname -g srg -o json
 
            url="https://management.azure.com/" + id + "/databases"
            
            params = {'api-version': '2017-10-01-preview'}
            r = requests.get(url, headers=headers, params=params)
            
            azr2= r.json()["value"]
            if cde:
                print(json.dumps(azr2, indent=4, separators=(',', ': ')))

            icount=len(azr2)
            if icount > 0 :
                for j in range(0,icount):
        
                    name = azr2[j]["name"]
                    loc = azr2[j]["location"]
                    id = azr2[j]["id"]
                    rg = id.split("/")[4].replace(".", "-").lower()
                    rgs = id.split("/")[4]
                    if crg is not None:
                        if rgs.lower() != crg.lower():
                            continue  # back to for

                    rname = name.replace(".", "-")
                    prefix = tfp+"."+rg+'__'+rname
                    # print prefix
                    rfilename = prefix+".tf"
                    fr = open(rfilename, 'w')
                    fr.write(az2tfmess)
                    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                    fr.write('\t name = "' + name + '"\n')
                    fr.write('\t location = "' + loc + '"\n')
                    fr.write('\t resource_group_name = "' + rgs + '"\n')
                    #fr.write('\t server_name = "' + sname + '"\n')
                    col=azr2[j]["properties"]["collation"]
                    ed=azr2[j]["properties"]["currentSku"]["tier"]
                    rso=azr2[j]["properties"]["requestedServiceObjectiveName"]
                    fr.write('\t server_name = "' + sname + '"\n')
                    if ed != "System":
                        
                        fr.write('\t collation= "' + col + '"\n')
                        fr.write('\t edition= "' + ed + '"\n')
                        fr.write('\t requested_service_objective_name= "' + rso + '"\n')
                        try:
                            cm = azr2[j]["properties"]["createMode"]
                            fr.write('\t create_mode= "' + cm + '"\n')
                        except KeyError:
                            pass

            # tags block
                    try:
                        mtags = azr2[j]["tags"]
                        fr.write('tags = { \n')
                        for key in mtags.keys():
                            tval = mtags[key]
                            fr.write(('\t "' + key + '"="' + tval + '"\n'))
                        fr.write('}\n')
                    except KeyError:
                        pass

                    fr.write('}\n')
                    fr.close()   # close .tf file

                    if cde:
                        with open(rfilename) as f:
                            print (f.read())

                    tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                    tfim.write('echo "importing ' + str(i) +
                            ' of ' + str(count-1) + '"' + '\n')
                    tfcomm = 'terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                    tfim.write(tfcomm)

        # end for i loop

        tfrm.close()
        tfim.close()
    # end stub
 
#
# azurerm_databricks_workspace
#
# azurerm_databricks_workspace
def azurerm_databricks_workspace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_databricks_workspace"
    tcode="550-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Databricks/workspaces"
        params = {'api-version': '2018-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')


            sku=azr[i]["sku"]["name"]
            if sku == "Standard" : sku="standard" 
            if sku == "Premium" : sku="premium" 

            fr.write('\t sku = "' +  sku + '"\n')
   
            outid=azr[i]["id"]
            #print  outid
            #evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname outid

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+outid+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_app_service_plan
#
# azurerm_app_service_plan
def azurerm_app_service_plan(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_app_service_plan"
    tcode="600-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST App Service Plan"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Web/serverfarms"
        params = {'api-version': '2018-02-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')
            
            tier=azr[i]["sku"]["tier"]
            size=azr[i]["sku"]["size"]
            kind=azr[i]["kind"]

            fr.write('\t kind = "' +  kind + '"\n')

            fr.write('\t sku {\n')
            fr.write('\t\t tier = "' +  tier + '"\n')
            fr.write('\t\t size = "' +  size + '"\n')
            fr.write('\t }\n')

            
    # geo location block
            
    #        icount= geol | | len(
    #        if icount > 0" :
    #            for j in range(0,icount):
    #                floc=azr[i]["failoverPolicies[j]["locationName"
    #                fop=azr[i]["failoverPolicies[j]["failoverPriority"]
    #                fr.write('\t geo_location {'   + '"\n')
    #                fr.write('\t location =    "floc" + '"\n')
    #                fr.write('\t failover_priority  = "' +    fop + '"\n')
    #                fr.write('}\n')
    #            
    #       

            
            #
            # No tags - used internally
       
            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_app_service
#
# azurerm_app_service
def azurerm_app_service(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_app_service"
    tcode="610-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST App Service"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Web/sites"
        params = {'api-version': '2018-02-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            kind=azr[i]["kind"]
            if kind == "functionapp": continue

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

    #azr=az webapp list -g rgsource -o json

            prg=azr[i]["properties"]["serverFarmId"].split("/")[4]
            pnam=azr[i]["properties"]["serverFarmId"].split("/")[8]
       
            appplid=azr[i]["properties"]["serverFarmId"]

            try:
                httpsonly=str(azr[i]["properties"]["httpsOnly"]).lower()
                fr.write('\t https_only = ' +  httpsonly + '\n')
            except KeyError:
                pass

            # case issues - so use resource id directly
            # fr.write('\t app_service_plan_id = "${azurerm_app_service_plan. + '__' + .id}'"' prg pnam + '"\n')
            fr.write('\t app_service_plan_id = "' +  appplid + '"\n')

    # geo location block
            
    #        icount= geol | | len(
    #        if icount > 0" :
    #            for j in range(0,icount):
    #                floc=azr[i]["failoverPolicies[j]["locationName"
    #                fop=azr[i]["failoverPolicies[j]["failoverPriority"]
    #                fr.write('\t geo_location {'   + '"\n')
    #                fr.write('\t location =    "floc" + '"\n')
    #                fr.write('\t failover_priority  = "' +    fop + '"\n')
    #                fr.write('}\n')
    #            
    #       

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass


            url="https://management.azure.com/" + id + "/config/appsettings/list"
            #print url
            params = {'api-version': '2018-02-01'}
            r = requests.post(url, headers=headers, params=params)
            appset= r.json()
            #print(json.dumps(appset, indent=4, separators=(',', ': ')))

            fr.write('\t app_settings = { \n')

            try:
                strcon=appset["properties"]["AzureWebJobsStorage"]
            except KeyError:
                pass

            try:
                vers=appset["properties"]["FUNCTIONS_EXTENSION_VERSION"]
            except KeyError:
                pass

            try:
                runfrompackage=appset["properties"]["WEBSITE_RUN_FROM_PACKAGE"]
                fr.write('\t WEBSITE_RUN_FROM_PACKAGE = "' + runfrompackage + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["WEBSITE_NODE_DEFAULT_VERSION"]
                fr.write('\t WEBSITE_NODE_DEFAULT_VERSION = "' + aval + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["FUNCTIONS_WORKER_RUNTIME"]
                fr.write('\t FUNCTIONS_WORKER_RUNTIME = "' + aval + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["APPINSIGHTS_INSTRUMENTATIONKEY"]
                fr.write('\t APPINSIGHTS_INSTRUMENTATIONKEY = "' + aval + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["mykey"]
                fr.write('\t mykey = "' + aval + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["myten"]
                fr.write('\t myten = "' + aval + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["usern"]
                fr.write('\t usern = "' + aval + '"\n')
            except KeyError:
                pass

                #if aname == "WEBSITE_CONTENTSHARE" or aname == "WEBSITE_CONTENTAZUREFILECONNECTIONSTRING":


            try:
                aval=appset["properties"]["AzureWebJobsDashboard"]
                if len(aval) > 3:
                    blog=True
            except KeyError:
                pass

            fr.write('\t }'  + '\n')

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_function_app
#
# azurerm_function_app
def azurerm_function_app(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_function_app"
    tcode="620-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Function App"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Web/sites"
        params = {'api-version': '2018-02-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):
            kind=azr[i]["kind"]

            if kind != "functionapp": continue
            
            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            https=azr[i]["properties"]["httpsOnly"]
    

            #prg=azr[i]["properties"]["serverFarmId"].split("/")[4].lower()
            #pnam=azr[i]["properties"]["serverFarmId"].split("/")[8]
       
            appplid=azr[i]["properties"]["serverFarmId"]
    


            # case issues - so use resource id directly
            # fr.write('\t app_service_plan_id = "${azurerm_app_service_plan. + '__' + .id}'"' prg pnam + '"\n')
            fr.write('\t app_service_plan_id = "' + appplid + '"\n')
    # dummy entry

            fr.write('\t https_only = ' + str(https).lower() + '\n')
            blog=False
            strcon=""


            url="https://management.azure.com/" + id + "/config/appsettings/list"
            #print url
            params = {'api-version': '2018-02-01'}
            r = requests.post(url, headers=headers, params=params)       
            appset= r.json()
            #print(json.dumps(appset, indent=4, separators=(',', ': ')))
            
            fr.write('\t app_settings = { \n')
                    
            try:
                strcon=appset["properties"]["AzureWebJobsStorage"]         
            except KeyError:
                pass 
                    
            try:
                vers=appset["properties"]["FUNCTIONS_EXTENSION_VERSION"]            
            except KeyError:
                pass
                    
            try:
                aval=appset["properties"]["WEBSITE_NODE_DEFAULT_VERSION"]  
                fr.write('\t WEBSITE_NODE_DEFAULT_VERSION = "' + aval + '"\n')     
            except KeyError:
                pass

            try:
                aval=appset["properties"]["FUNCTIONS_WORKER_RUNTIME"]  
                fr.write('\t FUNCTIONS_WORKER_RUNTIME = "' + aval + '"\n')     
            except KeyError:
                pass  

            try:
                aval=appset["properties"]["APPINSIGHTS_INSTRUMENTATIONKEY"]  
                fr.write('\t APPINSIGHTS_INSTRUMENTATIONKEY = "' + aval + '"\n')     
            except KeyError:
                pass  

            try:
                aval=appset["properties"]["mykey"]  
                fr.write('\t mykey = "' + aval + '"\n')     
            except KeyError:
                pass

            try:
                aval=appset["properties"]["myten"]  
                fr.write('\t myten = "' + aval + '"\n')     
            except KeyError:
                pass
                        
            try:
                aval=appset["properties"]["usern"]  
                fr.write('\t usern = "' + aval + '"\n')     
            except KeyError:
                pass              
                    
            #if aname == "WEBSITE_CONTENTSHARE" or aname == "WEBSITE_CONTENTAZUREFILECONNECTIONSTRING":
                        
                                      
            try:
                aval=appset["properties"]["AzureWebJobsDashboard"] 
                if len(aval) > 3:
                    blog=True
            except KeyError:
                pass
                    
            fr.write('\t }'  + '\n')

               
            if len(strcon) >= 3 :
                fr.write('\t storage_connection_string = "' + strcon + '" \n')
            else:
                fr.write('\t storage_connection_string = ""\n')
        
            fr.write('\t version = "' + vers + '"\n')
            fr.write('\t enable_builtin_logging = ' + str(blog).lower() + '\n')


    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_logic_app_workflow
#
# azurerm_dns_zone
def azurerm_logic_app_workflow(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_logic_app_workflow"
    tcode="630-"
    azr=""
    #cde=False
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Logic/workflows"
        #params = {'api-version': '2016-04-01'}
        params = {'api-version': '2016-06-01'}       
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

    ###############
    # specific code start
    ###############
            try:
                params=azr[i]["properties"]["definition"]["parameters"]
                #print params
                lp=len(params)
                if lp > 0:
                    fr.write('parameters = { \n') 
                    fr.write('"$connections" = "" \n') 
                    #fr.write(json.dumps(params))
                    fr.write('}\n')
            except KeyError:
                pass      


            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_logic_app_trigger_http_request
#
# azurerm_dns_zone
def azurerm_logic_app_trigger_http_request(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_logic_app_trigger_http_request"
    tcode="631-"
    azr=""
    #cde=False
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Logic/workflows"
        #params = {'api-version': '2016-04-01'}
        params = {'api-version': '2016-06-01'}       
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):
            try:
                ttype=azr[i]["properties"]["definition"]["triggers"]["manual"]["kind"]
                if ttype != "Http":
                    continue




                name=azr[i]["name"]
                loc=azr[i]["location"]
                id=azr[i]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if rg[0].isdigit(): rg="rg_"+rg
                rgs=id.split("/")[4]


                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for
                if cde:
                    print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
                




                rname=name.replace(".","-")
                prefix=tfp+"."+rg+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')

                fr.write('\t logic_app_id = "${azurerm_logic_app_workflow.' + rg + '__' + rname + '.id}"' + '\n')

        ###############
        # specific code start
        ###############
                try:
                    params=azr[i]["properties"]["definition"]["triggers"]["manual"]["inputs"]["schema"]
                    #print(json.dumps(params, indent=4, separators=(',', ': ')))
                    fr.write('schema = jsonencode(\n') 
                    fr.write(json.dumps(params, indent=4, separators=(',', ': ')))
                    fr.write(')\n')
                except KeyError:
                    pass      

        

                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'/triggers/' + name +'\n'
                tfim.write(tfcomm)  

            except KeyError:
                pass
        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
 
#
# azurerm_monitor_autoscale_setting
#
# azurerm_monitor_autoscale_setting
import ast


def azurerm_monitor_autoscale_setting(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp = "azurerm_monitor_autoscale_setting"
    tcode = "650-"
    azr = ""
    
    if crf in tfp:
        # REST or cli
        # print "REST monitor autoscale"
        url = "https://" + cldurl + "/subscriptions/" + \
            sub + "/providers/microsoft.insights/autoscalesettings"
        params = {'api-version': '2015-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr = r.json()["value"]

        tfrmf = tcode+tfp+"-staterm.sh"
        tfimf = tcode+tfp+"-stateimp.sh"
        tfrm = open(tfrmf, 'a')
        tfim = open(tfimf, 'a')
        print ("# " + tfp,)
        count = len(azr)
        print (count)
        for i in range(0, count):

            name = azr[i]["name"]
            loc = azr[i]["location"]
            id = azr[i]["id"]
            rg = id.split("/")[4].replace(".", "-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs = id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))

            rname = name.replace(".", "-")
            rname = name.replace(" ", "-")
            prefix = tfp+"."+rg+'__'+rname
            #print prefix
            rfilename = prefix+".tf"
            fr = open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('name = "' + name + '"\n')
            fr.write('location = "' + loc + '"\n')
            fr.write('resource_group_name = "' + rgs + '"\n')

            en = azr[i]["properties"]["enabled"]
            

    # basic settings

            fr.write('enabled = ' + str(en).lower() + '\n')

            try:
                triid = azr[i]["properties"]["targetResourceUri"]
                parts = triid.split("/")
                #print "parts=" + str(len(parts))
                trrg = azr[i]["properties"]["targetResourceUri"].split(
                    "/")[4].replace(".", "-").lower()
                trty = azr[i]["properties"]["targetResourceUri"].split(
                    "/")[6].replace(".", "-")
                trid = azr[i]["properties"]["targetResourceUri"].split(
                    "/")[8].replace(".", "-")
                # assume trty = Microsoft.Compute
                tftyp = "azurerm_virtual_machine_scale_set"
                if trty == "Microsoft-Web":
                    tftyp = "azurerm_app_service_plan"
                # case sensitite so use actual ID
                fr.write('target_resource_id = "' + triid + '"\n')
                #fr.write('target_resource_id = "${'+ tftyp + '.' + trrg + '__' + trid+'.id}"\n')
            except KeyError:
                pass

    #  profiles block
            try:
                profs = azr[i]["properties"]["profiles"]
                icount = len(profs)
                if icount > 0:
                    for j in range(0, icount):
                        fr.write('profile {\n')
                        pn = azr[i]["properties"]["profiles"][j]["name"]
                        pn = pn.replace('"', '\\"')
                        # pn="dummy"
                        # pn=pn.replace('{','\{')
                        cdef = azr[i]["properties"]["profiles"][j]["capacity"]["default"]
                        cmin = azr[i]["properties"]["profiles"][j]["capacity"]["minimum"]
                        cmax = azr[i]["properties"]["profiles"][j]["capacity"]["maximum"]
                        fr.write('\tname =  "'+pn + '"\n')
        # capacity
                        fr.write('\tcapacity {\n')
                        fr.write('\t\tdefault = "' + cdef + '"\n')
                        fr.write('\t\tminimum = "' + cmin + '"\n')
                        fr.write('\t\tmaximum = "' + cmax + '"\n')
                        fr.write('\t}\n')
        # fixed date

                        try:
                            fd = azr[i]["properties"]["profiles"][j]["fixedDate"]["end"]
                            fdend = azr[i]["properties"]["profiles"][j]["fixedDate"]["end"]
                            fdstart = azr[i]["properties"]["profiles"][j]["fixedDate"]["start"]
                            fdtz = azr[i]["properties"]["profiles"][j]["fixedDate"]["timeZone"]
                            fdend2 = fdend.split("+")[0]
                            fdstart2 = fdstart.split("+")[0]
                            fr.write('\tfixed_date {\n')
                            fr.write('\t\ttimezone =  "' + fdtz + '"\n')
                            fr.write('\t\tstart = "' + fdstart2 + '"\n')
                            fr.write('\t\tend = "' + fdend2 + '"\n')
                            fr.write('\t}\n')
                        except KeyError:
                            pass

        # recurance

                        try:
                            rec = azr[i]["properties"]["profiles"][j]["recurrence"]
                            rfr = azr[i]["properties"]["profiles"][j]["recurrence"]["frequency"]
                            # dns=str(ast.literal_eval(json.dumps(azr[i]["properties"]["dhcpOptions"]["dnsServers"])))
                            # dns=dns.replace("'",'"')

                            rsd = str(ast.literal_eval(json.dumps(
                                azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["days"])))
                            rsd = rsd.replace("'", '"')
                            rsh = str(ast.literal_eval(json.dumps(
                                azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["hours"])))
                            rsh = rsh.replace("'", '"')
                            rsm = str(ast.literal_eval(json.dumps(
                                azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["minutes"])))
                            rsm = rsm.replace("'", '"')
                            rst = azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["timeZone"]
                            fr.write('\trecurrence {\n')
                            fr.write('\t\ttimezone = "' + rst + '"\n')
                            fr.write('\t\tdays =  ' + rsd + '\n')
                            fr.write('\t\thours =  ' + rsh + '\n')
                            fr.write('\t\tminutes =  ' + rsm + '\n')
                            fr.write('\t}\n')
                        except KeyError:
                            pass

        # rules block
                        try:
                            rules = azr[i]["properties"]["profiles"][j]["rules"]
                            kcount = len(rules)
                            #print "count of rules= "+str(kcount)
                            for k in range(0, kcount):
                                #print k
                                fr.write('\trule  {\n')
                                # metric trigger
                                mtn = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["metricName"]
                                if mtn == "CPU":
                                    mtn = "Percentage CPU"

                                mtid = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["metricResourceUri"]
                                mtrrg = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["metricResourceUri"].split(
                                    "/")[4].replace(".", "-").lower()
                                mtrid = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["metricResourceUri"].split(
                                    "/")[8].replace(".", "-")
                                mtop = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["operator"]
                                mtstat = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["statistic"]
                                mtthres = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["threshold"]
                                mtta = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["timeAggregation"]
                                mttg = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["timeGrain"]
                                mttw = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["timeWindow"]
                                mttg2 = mttg
                                mttw2 = mttw
                                #print mtthres
                                # mttg2= mttg.split(":")[1].replace("0","") # sed 's/^0*//'
                                # mttw2= mttw.split(":")[1].replace("0","") #| cut -f2 -d':' | sed 's/^0*//'

                                # metric trigger block
                                fr.write('\t\tmetric_trigger {\n')
                                fr.write('\t\t\tmetric_name = "' + mtn + '"\n')
                                fr.write(
                                    '\t\t\tmetric_resource_id = "${'+tftyp + '.' + mtrrg + '__' + mtrid + '.id}"\n')
                                fr.write('\t\t\toperator = "' + mtop + '"\n')
                                fr.write('\t\t\tstatistic= "' + mtstat + '"\n')
                                fr.write('\t\t\tthreshold = "' +
                                        str(mtthres) + '"\n')
                                fr.write(
                                    '\t\t\ttime_aggregation = "' + mtta + '"\n')
                                fr.write('\t\t\ttime_grain = "' + mttg2 + '"\n')
                                fr.write('\t\t\ttime_window = "' + mttw2 + '"\n')
                                fr.write('\t\t}\n')

                                # scale action block
                                sac = azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["cooldown"]
                                sad = azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["direction"]
                                sat = azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["type"]
                                sav = azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["value"]

                                fr.write('\t\tscale_action  {\n')
                                #print sac
                                # sac2= sac.split(":")[1].replace("0","") #| cut -f2 -d':' | sed 's/^0*//'
                                sac2 = sac
                                fr.write('\t\t\tcooldown = "' + sac2 + '"\n')
                                fr.write('\t\t\tdirection = "' + sad + '"\n')
                                fr.write('\t\t\ttype = "' + sat + '"\n')
                                fr.write('\t\t\tvalue = "' + sav + '"\n')
                                fr.write('\t\t}\n')

                                fr.write('\t}\n')  # end rule
                        except KeyError:
                            pass

                        fr.write('}\n')  # end profile
            except KeyError:
                pass
# notification block
            try:
                nots = azr[i]["properties"]["notifications"]
                ncount = len(nots)
                #print "num notifications=" + str(ncount)
                for k in range(0, ncount):
                    #print "k="+str(k)
                    nsa = azr[i]["properties"]["notifications"][k]["email"]["sendToSubscriptionAdministrator"]
                    #print "nsa "+str(nsa)
                    nsca = azr[i]["properties"]["notifications"][k]["email"]["sendToSubscriptionCoAdministrators"]
                    #print "nsca "+str(nsca)
                    nce = str(ast.literal_eval(json.dumps(azr[i]["properties"]["notifications"][k]["email"]["customEmails"])))
                    nce = nce.replace("'", '"')
                    #print "nce= "+str(nce)
                    fr.write('notification {\n')
                    fr.write('\temail {\n')

                    
                    fr.write('\t\tsend_to_subscription_administrator = ' + str(nsa).lower() + '\n')

                    
                    fr.write('\t\tsend_to_subscription_co_administrator =  ' + str(nsca).lower() + '\n')

                    fr.write('\t\tcustom_emails =   '+nce+'\n')
                    fr.write('\t}\n')
                    nwh = str(ast.literal_eval(json.dumps(
                        azr[i]["properties"]["notifications"][k]["webhooks"])))
                    nwh = nwh.replace("'", '"')
                    #fr.write('webhook =   '+nwh + '\n')
                    fr.write('}\n')
            
            except Exception as e: print(e)

                #pass

    # tags block
            try:
                mtags = azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval = mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n')
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f:
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) +
                       ' of ' + str(count-1) + '"' + '\n')
            tfcomm = 'terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)

        # end for i loop

        tfrm.close()
        tfim.close()
    # end stub
 
#
# azurerm_api_management
#
# azurerm_api_management
def azurerm_api_management(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_api_management"
    tcode="640-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Function App"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.ApiManagement/service"
        params = {'api-version': '2019-01-01'}
        r = requests.get(url, headers=headers, params=params)
        try:
            azr= r.json()["value"]
        except KeyError:
            print ("Skipping api_management for now...")
            return
        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            
            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            pubn=azr[i]["properties"]["publisherName"]
            pube=azr[i]["properties"]["publisherEmail"]
            skun=azr[i]["sku"]["name"]
            skuc=azr[i]["sku"]["capacity"]

            fr.write('\t publisher_name = "'+ pubn + '"\n')
            fr.write('\t publisher_email = "'+ pube + '"\n')
            fr.write('sku  { \n')
            fr.write('\t name = "'+ skun + '"\n')
            fr.write('\t capacity = "'+ str(skuc) + '"\n')
            fr.write('} \n')

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

 
#
# azurerm_policy_definition
#
import ast
def azurerm_policy_definition(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):  
    tfp="azurerm_policy_definition"
    
    azr=""
    if crf in tfp:
    # REST or cli
        #print "REST Pol Defn"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Authorization/policyDefinitions"
        params = {'api-version': '2019-01-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="004-"+tfp+"-staterm.sh"
        tfimf="004-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            #loc=azr[i]["location"]
            id=azr[i]["id"]
            rg="policydefinitions"
            rgs=id.split("/")[4]
          
            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for

            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            pt=azr[i]["properties"]["policyType"]
            if pt == "Custom" :

                if cde:
                    print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                #fr.write('\t location = "'+ loc + '"\n')
                #fr.write('\t resource_group_name = "'+ rgs + '"\n')

                rdid=azr[i]["name"]            
                mode=azr[i]["properties"]["mode"]
                rg="policyDefinitions"
                                

                
                try :
                    dname=azr[i]["properties"]["displayName"]
                    fr.write('display_name =  "'+dname+'"\n') 
                except KeyError:
                    fr.write('display_name = ""\n')
                    pass
            
                fr.write('policy_type = "' + pt +'"\n') 
                fr.write('mode = "' + mode + '"\n') 
                try :
                    desc=azr[i]["properties"]["description"]
                    fr.write('description =  "'+desc +'"\n') 
                except KeyError:
                    pass   
     
                #print(json.dumps(azr[i]["properties"]["metadata"], indent=4, separators=(',', ': ')))
                
                fr.write('metadata = jsonencode(\n') 
                fr.write(json.dumps(azr[i]["properties"]["metadata"]))
                fr.write(') \n') 

                prules=str(ast.literal_eval(json.dumps(azr[i]["properties"]["policyRule"])))
                fr.write('policy_rule = jsonencode( \n')
                fr.write(json.dumps(azr[i]["properties"]["policyRule"]))  
                fr.write(') \n') 
                
                try:
                    params=azr[i]["properties"]["parameters"]          
                    pl= len(params)
                    if pl > 0 :
                        fr.write('parameters = jsonencode( \n') 
                        fr.write(json.dumps(azr[i]["properties"]["parameters"])) 
                        fr.write(') \n') 
                except KeyError:
                    pass

                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub 
#
# azurerm_policy_set_definition
#
import ast

def azurerm_policy_set_definition(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp = "azurerm_policy_set_definition"
    
    azr = ""
    if crf in tfp:
        # REST or cli
        #print "REST Pol Defn"
        url = "https://" + cldurl + "/subscriptions/" + sub + \
            "/providers/Microsoft.Authorization/policySetDefinitions"
        params = {'api-version': '2019-01-01'}
        r = requests.get(url, headers=headers, params=params)
        azr = r.json()["value"]

        tfrmf = "008-"+tfp+"-staterm.sh"
        tfimf = "008-"+tfp+"-stateimp.sh"
        tfrm = open(tfrmf, 'a')
        tfim = open(tfimf, 'a')
        print ("# " + tfp,)
        count = len(azr)
        print (count)
        for i in range(0, count):

            name = azr[i]["name"]
            # loc=azr[i]["location"]
            id = azr[i]["id"]
            rg = "policysetdefinitions"
            rgs = id.split("/")[4]

            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for

            rname = name.replace(".", "-")
            prefix = tfp+"."+rg+'__'+rname
            #print prefix
            pt = azr[i]["properties"]["policyType"]
            if pt != "BuiltIn" :
                if cde:
                    print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
                rfilename = prefix+".tf"
                fr = open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                    #fr.write('\t location = "'+ loc + '"\n')
                    #fr.write('\t resource_group_name = "'+ rgs + '"\n')

                rdid = azr[i]["name"]            
                pt = azr[i]["properties"]["policyType"]
                rg = "policySetDefinitions"


                try:
                    dname = azr[i]["properties"]["displayName"]
                    fr.write('display_name =  "'+dname+'"\n')
                except KeyError:
                    fr.write('display_name = ""\n')
                    pass

                fr.write('policy_type = "' + pt + '"\n') 
                #fr.write('mode = "' + mode + '"\n')
                try:
                    desc = azr[i]["properties"]["description"]
                    desc=desc.replace('\\','\\\\')
                    fr.write('description =  "'+desc + '"\n') 
                except KeyError:
                    pass

                #print(json.dumps(azr[i]["properties"]["metadata"], indent=4, separators=(',', ': ')))


                try:
                    params = azr[i]["properties"]["parameters"]          
                    pl = len(params)
                    if pl > 0:
                        fr.write('parameters = jsonencode( \n')
                        fr.write(json.dumps(params))
                        fr.write(') \n')
                except KeyError:
                    pass


                try:
                    pdef = str(ast.literal_eval(json.dumps(azr[i]["properties"]["policyDefinitions"])))
                    fr.write('policy_definitions= jsonencode( \n')
                    fr.write(json.dumps(pdef))
                    fr.write(') \n')
                    #pcount=len(pdef)             
                    #for p in range(0, pcount):
                    #    fr.write('policy_definitions= jsonencode( \n')
                    #    fr.write(json.dumps(pdef[p]))
                    #    fr.write(') \n')
                    
                except KeyError:
                    pass
        

                fr.write('}\n')
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f:
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm = 'terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)

        # end for i loop

        tfrm.close()
        tfim.close()
    # end stub
 
#
# azurerm_policy_assignment
#

def azurerm_policy_assignment(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    
    tfp="azurerm_policy_assignment"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Authorization/policyAssignments"
        params = {'api-version': '2019-01-01'}

        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="005-"+tfp+"-staterm.sh"
        tfimf="005-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            #loc=azr[i]["location"]
            id=azr[i]["id"]
            rg="policyassignments"
            rg=id.split("/")[4].replace(".","-").lower()
            rgs=id.split("/")[4]
            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            try:
                loc=azr[i]["location"]
                fr.write('\t location = "'+ loc + '"\n')
            except KeyError:
                pass
            #fr.write('\t resource_group_name = "'+ rgs + '"\n')

    ###############
    # specific code
           
            dname=azr[i]["properties"]["displayName"]
            rdid=azr[i]["name"]
           
            scope=azr[i]["properties"]["scope"]
            pdid=azr[i]["properties"]["policyDefinitionId"]
            id=azr[i]["id"]

            

                
            fr.write('display_name = "' + dname +'"\n') 
            fr.write('policy_definition_id = "' + pdid +'"\n') 
            fr.write('scope = "' +  scope +'"\n') 
            try :
                desc=azr[i]["properties"]["description"]
                fr.write('description =  "'+desc +'"\n') 
            except KeyError:
                pass
            
            try:
                params=azr[i]["properties"]["parameters"]
                pl=len(params)
                #print pl
                #print(json.dumps(azr[i]["properties"]["parameters"]))
                if pl > 0 :
                    fr.write('parameters = jsonencode( \n') 
                    fr.write(json.dumps(azr[i]["properties"]["parameters"]))
                    fr.write(')\n') 
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub 
#
# azurerm_role_definition
#
import ast
def azurerm_role_definition(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_role_definition"
    
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Authorization/roleDefinitions"

        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="006-"+tfp+"-staterm.sh"
        tfimf="006-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            #loc=azr[i]["location"]
            id=azr[i]["id"]
            rg="roledefinitions"
            rgs=id.split("/")[4]
            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            
            #fr.write('\t location = "'+ loc + '"\n')
            #fr.write('\t resource_group_name = "'+ rgs + '"\n')
            
            name=azr[i]["properties"]["roleName"]
            fr.write('\t name = "' + name + '"\n')
            rdid=azr[i]["name"]
            desc=azr[i]["properties"]["description"]
            #desc=desc.encode('utf-8', 'ignore')
            id=azr[i]["id"]
            

            scopes=azr[i]["properties"]["assignableScopes"]
            scopes=str(ast.literal_eval(json.dumps(azr[i]["properties"]["assignableScopes"])))
            scopes=scopes.replace("'",'"')
            dactions=azr[i]["properties"]["permissions"][0]["dataActions"]
            ndactions=azr[i]["properties"]["permissions"][0]["notDataActions"]
            actions=azr[i]["properties"]["permissions"][0]["actions"]
            nactions=azr[i]["properties"]["permissions"][0]["notActions"]

            #fr.write('role_definition_id = "' + rdid +  '"\n')
            fr.write('description =  "' +desc + '"\n')
            #fr.write('scope = "'\{'data.azurerm_subscription.primary.id}'"'  '"\n')
            #fr.write('scope = "'/subscriptions/"' rgsource '"\n')
            fr.write('assignable_scopes = ' + scopes + '\n')
            fr.write('scope = ""\n')
            #
            
            
            fr.write('permissions {\n')        
            #print(json.dumps(dactions)) 
            fr.write('data_actions = ')
            fr.write(json.dumps(dactions))  
            
            fr.write('\nnot_data_actions = ')
            fr.write(json.dumps(ndactions)) 
        
            fr.write('\nactions = ')
            fr.write(json.dumps(actions)) 
        
            fr.write('\nnot_actions = ')
            fr.write(json.dumps(nactions)) 
            
            fr.write('\n}\n')
            """
            fr.write('assignable_scopes = \n')
            fr.write(json.dumps(scopes)) 
        
            """
            
            fr.write('\n}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub 
#
# azurerm_role_assignment
#

def azurerm_role_assignment(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    
    tfp="azurerm_role_assignment"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Authorization/roleAssignments"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="007-"+tfp+"-staterm.sh"
        tfimf="007-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            #loc=azr[i]["location"]
            id=azr[i]["id"]
            rg="roleassignments"
            rgs=id.split("/")[4]
            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            #fr.write('\t location = "'+ loc + '"\n')
            #fr.write('\t resource_group_name = "'+ rgs + '"\n')

            name=azr[i]["name"]
        
            scope=azr[i]["properties"]["scope"]
            rdid=azr[i]["name"]
            prid=azr[i]["properties"]["principalId"]
            roledefid=azr[i]["properties"]["roleDefinitionId"].split("/")[6]
            id=azr[i]["id"]
          

            fr.write('role_definition_id = "${azurerm_role_definition.' + "roledefinitions" + '__' + roledefid + '.id}"' + '\n')
            
            fr.write('principal_id ="' +prid +'"\n') 
            fr.write('scope = "' + scope  +'"\n') 
    
            #fr.write('}\n')

       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub# RUNBOOK ON
#
# runbook get token
#
runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
bt=get_automation_runas_token()
sub=str(runas_connection["SubscriptionId"])
headers = {'Authorization': 'Bearer ' + bt, 'Content-Type': 'application/json'}
crg=None
crf="azurerm"
cde=False
az2tfmess="# File generated by az2tf see: https://github.com/andyt530/az2tf \n"
 

# record and sort resources - no longer needed
# azure_resources.azure_resources(crf,cde,crg,headers,requests,sub,json,az2tfmess,os)
# 001 Resource Group
azurerm_resource_group(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 002 management lock
azurerm_management_lock(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 015 user assigned identity
azurerm_user_assigned_identity(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 020 Avail Sets
azurerm_availability_set(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 030 Route Table
azurerm_route_table(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 040 ASG
azurerm_application_security_group(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 050 NSG's
azurerm_network_security_group(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 060 Virtual Networks
azurerm_virtual_network(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 070 subnets
azurerm_subnet(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 080 vnet peering
azurerm_virtual_network_peering(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 090 Key Vault - using cli
azurerm_key_vault(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 100 managed disk
azurerm_managed_disk(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 110 storgae account
azurerm_storage_account(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 120 public ip
azurerm_public_ip(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 124 Traffic manager profile
azurerm_traffic_manager_profile(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 125 traffic manager endpoint
azurerm_traffic_manager_endpoint(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 130 network interface
azurerm_network_interface(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 131_azurerm_dns_zone
azurerm_dns_zone(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 140_azurerm_lb
azurerm_lb(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 150_azurerm_lb_nat_rule
azurerm_lb_nat_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 160_azurerm_lb_nat_pool
azurerm_lb_nat_pool(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 170_azurerm_lb_backend_address_pool
azurerm_lb_backend_address_pool(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 180_azurerm_lb_probe
azurerm_lb_probe(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 190_azurerm_lb_rule
azurerm_lb_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 193_azurerm_application_gateway
azurerm_application_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 200_azurerm_local_network_gateway
azurerm_local_network_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 210_azurerm_virtual_network_gateway
azurerm_virtual_network_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 220_azurerm_virtual_network_gateway_connection
azurerm_virtual_network_gateway_connection(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 230_azurerm_express_route_circuit
azurerm_express_route_circuit(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 240_azurerm_express_route_circuit_authorization
azurerm_express_route_circuit_authorization(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 250_azurerm_express_route_circuit_peering
azurerm_express_route_circuit_peering(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 260_azurerm_container_registry
azurerm_container_registry(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 270_azurerm_kubernetes_cluster
azurerm_kubernetes_cluster(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 280_azurerm_recovery_services_vault
azurerm_recovery_services_vault(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 290_azurerm_virtual_machine
azurerm_virtual_machine(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 290_azurerm_virtual_machine_extension
azurerm_virtual_machine_extension(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 295_azurerm_virtual_machine_scale_set
azurerm_virtual_machine_scale_set(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 310_azurerm_automation_account
azurerm_automation_account(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 320_azurerm_log_analytics_workspace
azurerm_log_analytics_workspace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 330_azurerm_log_analytics_solution
azurerm_log_analytics_solution(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 340_azurerm_image
azurerm_image(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)

# 341_azurerm_shared_image_gallery
azurerm_shared_image_gallery(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
azurerm_shared_image(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
azurerm_shared_image_version(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 350_azurerm_snapshot
azurerm_snapshot(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 360_azurerm_network_watcher
azurerm_network_watcher(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 400_azurerm_cosmosdb_account
azurerm_cosmosdb_account(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 500_azurerm_servicebus_namespace
azurerm_servicebus_namespace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 510_azurerm_servicebus_queue
azurerm_servicebus_queue(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 520_azurerm_eventhub_namespace
azurerm_eventhub_namespace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 521_azurerm_eventhub
azurerm_eventhub(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 522_azurerm_eventhub_namespace_authorization_rule
azurerm_eventhub_namespace_authorization_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 540_azurerm_sql_server
azurerm_sql_server(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 541_azurerm_sql_database
azurerm_sql_database(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
if ccld != 'AzureChinaCloud':
# 550_azurerm_databricks_workspace
azurerm_databricks_workspace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 600_azurerm_app_service_plan
azurerm_app_service_plan(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 610_azurerm_app_service
azurerm_app_service(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)

# 620_azurerm_function_app
azurerm_function_app(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)

# 630_azurerm_logic_app_workflow
azurerm_logic_app_workflow(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)


# 640_azurerm_api_management
azurerm_api_management(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)

# 631_azurerm_logic_app_trigger_http_request
# AWAITING terraform import fix
#azurerm_logic_app_trigger_http_request.azurerm_logic_app_trigger_http_request(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)

if ccld != 'AzureChinaCloud':
# 650_azurerm_monitor_autoscale_setting
azurerm_monitor_autoscale_setting(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)

# az2tf-runbook.py gen-runbook.sh inline not.py run.py
tffile="*.tf"
fileList = glob.glob(tffile) 
# Iterate over the list of filepaths & remove each file.
for filePath in fileList:
    with open(filePath) as f: 
        print (f.read())

tffile="*stateimp.sh"
fileList = glob.glob(tffile) 
# Iterate over the list of filepaths & remove each file.
for filePath in fileList:
    with open(filePath) as f: 
        print (f.read())
print "# END \n"