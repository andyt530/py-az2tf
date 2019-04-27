prefixa=print 0 | awk -F 'azurerm_' '{'print 2}'' | cut -f1 -d'.'
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
azr=az sql server list -g rgsource -o json
count=print azr | jq '. | length'
if count" != "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        loc=azr[i]["location"]
        ver=azr[i]["version"]
        al=azr[i]["administratorLogin"]
        ap=azr[i]["administratorLoginPassword"]


        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t version = "' +  ver + '"\n')
        fr.write('\t administrator_login= "' +  al + '"\n')
        
        if ap" != "null" :
            fr.write('\t administrator_login_password= "' +  ap + '"\n')
        else
            fr.write('\t administrator_login_password= "' +   + '"\n')
        fi

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
     
        #
        fr.write('}' + '"\n')
        #
        cat outfile
        statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
        print statecomm >> tf-staterm.sh
        eval statecomm
        evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname id
        print evalcomm >> tf-stateimp.sh
        eval evalcomm
        
    
fi
