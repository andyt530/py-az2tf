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