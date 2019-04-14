tfp="azurerm_lb"
prefixa="lb"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az network lb list -g $rgsource`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
    name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
    rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`  
    id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
    loc=`echo $azr | jq ".[(${i})].location"`

    prefix=`printf "%s__%s" $prefixa $rg`

    printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
    printf "\t name = \"%s\"\n" $name >> $prefix-$name.tf
    printf "\t location = %s\n" "$loc" >> $prefix-$name.tf
    printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
    printf "}\n" >> $prefix-$name.tf
    #
    cat $prefix-$name.tf
    statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $name`
    echo $statecomm >> tf-staterm.sh
    eval $statecomm
    evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $name $id`
    echo $evalcomm >> tf-stateimp.sh
    eval $evalcomm
    
done
fi
