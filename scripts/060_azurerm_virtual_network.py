
#
azr=az network vnet list -g rgsource -o json
#
# loop around vnets
#
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):

        print az2tfmess > outle

        dns=azr[i]["dhcpOptions.dnsServers"
        addsp=azr[i]["addressSpace.addressPrexes"
 
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\tname = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        #fr.write('\t resource_group_name = "'\{'var.rgtarget}'"'  + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        if dns" != "null" :
            fr.write('\t dns_servers =  "dns" + '"\n')
        

        fr.write('\taddress_space =  "addsp" + '"\n')
        #
        #loop around subnets
        #
        subs=azr[i]["subnets"
        count=print subs | jq '. | length'
        count=expr count - 1
        for j in range( 0 count):
            snname=print subs | jq ".[j]["name"
            snaddr=print subs | jq ".[j]["addressPrex"
            snnsgid=print subs | jq ".[j]["networkSecurityGroup.id"
            nsgnam=print snnsgid | cut -d'/' -f9 | sed 's/\./-/g']
            nsgrg=print snnsgid | cut -d'/' -f5 | sed 's/\./-/g']
            fr.write('\tsubnet {'  + '"\n')
            fr.write('\t\t name =  snname + '"\n')
            fr.write('\t\t address_prex =  snaddr + '"\n')
            if nsgnam" != "null" :
                fr.write('\t\t security_group = "'\{'azurerm_network_security_group. + '__' + .id}'"' nsgrg nsgnam + '"\n')
            
            fr.write('\t}' + '"\n')          
        

        

        print "}'" + '"\n')
        #
        #

    

