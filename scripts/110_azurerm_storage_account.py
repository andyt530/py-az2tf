


        satier=azr[i]["sku.tier"]
        sakind=azr[i]["kind"]
        sartype=azr[i]["sku.name" | cut -f2 -d'_']
        saencrypt=azr[i]["encryption.services.blob.enabled"]
        fiencrypt=azr[i]["encryption.services.file.enabled"]
        sahttps=azr[i]["enableHttpsTrafficOnly"]
        nrs=azr[i]["networkRuleSet"
        saencs=azr[i]["encryption.keySource"]
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t account_tier = "' +  satier + '"\n')
        fr.write('\t account_kind = "' +  sakind + '"\n')
        fr.write('\t account_replication_type = "' +  sartype + '"\n')
        fr.write('\t enable_blob_encryption = "' +  saencrypt + '"\n')
        fr.write('\t enable_file_encryption = "' +  fiencrypt + '"\n')
        fr.write('\t enable_https_traffic_only = "' +  sahttps + '"\n')
        fr.write('\t account_encryption_source = "' +  saencs + '"\n')
        
        if nrs.bypass" != "null" :
            byp=azr[i]["networkRuleSet.bypass"]
            ipr=azr[i]["networkRuleSet.ipRules"
            vnr=azr[i]["networkRuleSet.virtualNetworkRules"

            icount=print ipr | jq '. | length'
            vcount=print vnr | jq '. | length'
            
            # if the only network rule is AzureServices, dont need a network_rules block
            if byp" != "AzureServices" ]["|| [ "icount" -gt "0" ]["|| [ "vcount" -gt "0" :
                fr.write('\t network_rules {'  + '"\n')
                byp=print byp | tr -d ','
                fr.write('\t\t bypass = ["' + ]["n" byp + '"\n')

                if icount" -gt "0" :
                    icount=expr icount - 1
                    for ic in range( 0 icount): 
                        ipa=print ipr | jq ".[ic]["ipAddressOrRange"]
                        fr.write('\t\t ip_rules = ["' + ]["n" ipa + '"\n')
                    
                fi
                
                if vcount" -gt "0" :
                    vcount=expr vcount - 1
                    for vc in range( 0 vcount):
                        vnsid=print vnr | jq ".[vc]["virtualNetworkResourceId"]
                        fr.write('\t\t virtual_network_subnet_ids = ["' + ]["n" vnsid + '"\n')
                    
                fi

                fr.write('\t }'  + '"\n')
            fi
        fi



