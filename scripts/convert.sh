echo "converting $1"
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
sed -i .bak -e 's/done//g' $1
sed -i .bak -e 's/ fi //g' $1
sed -i .bak -e 's/then/:/g' $1
sed -i .bak -e 's/=echo/=/g' $1
sed -i .bak -e 's/\}'\'' + '\''\"/\}/g' $1
sed -i .bak -e 's/!= \"null\"/try/g' $1
sed -i .bak -e 's/ | cut -d'\''\/'\'' -f5/].split(\"\/\")[4]/g' $1
sed -i .bak -e 's/ | cut -d'\''\/'\'' -f9/].split(\"\/\")[8]/g' $1
sed -i .bak -e 's/ | cut -d'\''\/'\'' -f11/].split(\"\/\")[10]/g' $1
sed -i .bak -e 's/length'\''/len(/g' $1
sed -i .bak -e 's/] | sed '\''s\/\\.\/-\/g'\'']/].replace(\".\",\"-\")/g' $1
sed -i .bak -e 's/ | sed '\''s\/\\.\/-\/g'\'']/].replace(\".\",\"-\")/g' $1
sed -i .bak -e 's/ | sed '\''s\/\\.\/-\/g'\''/.replace(\".\",\"-\")/g' $1
sed -i .bak -e 's/.id\"]/\"]["id\"]'/g $1
sed -i .bak -e 's/[[:space:]]fi//g' $1
sed -i .bak -e 's/range( 0 /range(0,/g' $1 
sed -i .bak -e '/prefix=/d' $1
sed -i .bak -e '/outfile=/d' $1
sed -i .bak -e '/=expr /d' $1
sed -i .bak -e '/echo az2tfmess/d' $1
sed -i .bak -e 's/ jq '\''.//g' $1
sed -i .bak -e 's/\" -gt \"/ > /g' $1
sed -i .bak -e 's/\"\[/\"\]\[/g' $1
rm -f *.bak

