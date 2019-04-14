i=0
for fn in `ls azurerm_network_security_group*.tf`; do
#sed s/resource \"azurerm_network_security_group\" \"rg-dwp-test-ch-pns-core__nsg-dwp-test-ch-pns-be01\" {/resource \"azurerm_network_security_group\" \"nsg\"/ > $fn.tmp
sed s/uksouth/\${var.location}/  $fn > $fn.tmp2
sed s/test-ch-pns/\${var.env}-\${var.director}-\${var.depd}/ $fn.tmp2 > $fn.tmp3
done