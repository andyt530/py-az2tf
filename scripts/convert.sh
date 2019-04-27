echo $1
sed -i .bak -e 's/\$//g' $1 
sed -i .bak -e 's/\`//g' $1 
sed -i .bak -e 's/\})//g' $1 
sed -i .bak -e 's/({//g' $1 
sed -i .bak -e 's/echo azr | jq "./azr/g' $1
sed -i .bak -e 's/]./]["/g' $1
sed -i .bak -e 's/ | tr -d '\''\"'\''/]/g' $1
sed -i .bak -e 's/printf \"/fr.write('\''/g' $1
sed -i .bak -e 's/\\n\"//g' $1
sed -i .bak -e 's/ >> outfile/ + '\''\"\\n'\'')/g' $1
sed -i .bak -e 's/%s//g' $1
sed -i .bak -e 's/\\\"/\"'\''/g' $1
sed -i .bak -e 's/__/ + '\''__'\'' + /g' $1
sed -i .bak -e 's/\}/\}'\''/g' $1 
sed -i .bak -e 's/{/{'\''/g' $1 
sed -i .bak -e 's/\"\"/\"/g' $1 
sed -i .bak -e 's/if \[ \"/if /g' $1
sed -i .bak -e 's/\]\[\" then/:/g' $1
sed -i .bak -e 's/\"'\''\"'\''/\"'\'' + /g' $1
sed -i .bak -e 's/; do/):/g' $1
sed -i .bak -e 's/in seq/in range(/g' $1
sed -i .bak -e 's/echo/print/g' $1
sed -i .bak -e 's/done//g' $1
sed -i .bak -e 's/ fi //g' $1
sed -i .bak -e 's/then/:/g' $1
