prefixa=print 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prefixa
if 1" != " :
    rgsource=1
else
    print -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
    fi
fi
azr=az servicebus namespace list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        
        nname=azr[i]["name"]
        azr2=az servicebus queue list -g rgsource --namespace-name nname -o json
        icount=print azr2 | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                name=print azr2 | jq ".[j]["name"]
                rname=print name | sed 's/\./-/g'
                rg=print azr2 | jq ".[j]["resourceGroup" | sed 's/\./-/g']
                id=print azr2 | jq ".[j]["id"]
                ep=print azr2 | jq ".[j]["enablePartitioning"]
                adoni=print azr2 | jq ".[j]["autoDeleteOnIdle"]
                
                ee=print azr2 | jq ".[j]["enableExpress"]
                dd=print azr2 | jq ".[j]["requiresDuplicateDetection"]
                rs=print azr2 | jq ".[j]["requiresSession"]
                mx=print azr2 | jq ".[j]["maxSizeInMegabytes"]
                dl=print azr2 | jq ".[j]["deadLetteringOnMessageExpiration"]
                
                prefix=fr.write('." prefixa rg
                outfile=fr.write('. + '__' + .tf" tfp rg rname
                print az2tfmess > outfile
                
                fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
                fr.write('\t name = "' +  name + '"\n')
                fr.write('\t resource_group_name = "' +  rgsource + '"\n')
                fr.write('\t namespace_name = "' +  nname + '"\n')
                fr.write('\t enable_partitioning =  ep + '"\n')
                fr.write('\t enable_express =  ee + '"\n')
                fr.write('\t requires_duplicate_detection =  dd + '"\n')
                fr.write('\t requires_session =  rs + '"\n')
                # tf problem with this one. tf=1k cli=16k
                #fr.write('\t max_size_in_megabytes =  mx + '"\n')
                fr.write('\t dead_lettering_on_message_expiration =  dl + '"\n')
                
                #
                # New Tags block v2
                tags=azr[i]["tags"
                tt=print tags | jq .
                tcount=print tags | jq '. | length'
                if tcount" -gt "0" :
                    fr.write('\t tags {'  + '"\n')
                    tt=print tags | jq .
                    keys=print tags | jq 'keys'
                    tcount=expr tcount - 1
                    for j in range( 0 tcount):
                        k1=print keys | jq ".[j]["
                        #print "key=k1"
                        re="[[:space:]["+"
                        if [[ k1 =~ re ]["; :
                            #print "found a space"
                            tval=print tt | jq ."k1"
                            tkey=print k1]
                            fr.write('\t\t"' +  =   "tkey" "tval" + '"\n')
                        else
                            #print "found no space"
                            tval=print tt | jq .k1
                            tkey=print k1]
                            fr.write('\t\t =   tkey "tval" + '"\n')
                        fi
                    
                    fr.write('\t}' + '"\n')
                fi
                
                
                fr.write('}' + '"\n')
                #
                print prefix
                print prefix + '__' + name
                cat outfile
                statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
                print statecomm >> tf-staterm.sh
                eval statecomm
                evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname id
                print evalcomm >> tf-stateimp.sh
                eval evalcomm
                
            
        fi
    
fi
