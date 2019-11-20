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
