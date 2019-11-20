# azurerm_monitor_autoscale_setting
import ast


def azurerm_monitor_autoscale_setting(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp = "azurerm_monitor_autoscale_setting"
    tcode = "650-"
    azr = ""
    
    if crf in tfp:
        # REST or cli
        # print "REST monitor autoscale"
        url = "https://" + cldurl + "/subscriptions/" + \
            sub + "/providers/microsoft.insights/autoscalesettings"
        params = {'api-version': '2015-04-01'}
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
            rgs = id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))

            rname = name.replace(".", "-")
            rname = name.replace(" ", "-")
            prefix = tfp+"."+rg+'__'+rname
            #print prefix
            rfilename = prefix+".tf"
            fr = open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('name = "' + name + '"\n')
            fr.write('location = "' + loc + '"\n')
            fr.write('resource_group_name = "' + rgs + '"\n')

            en = azr[i]["properties"]["enabled"]
            

    # basic settings

            fr.write('enabled = ' + str(en).lower() + '\n')

            try:
                triid = azr[i]["properties"]["targetResourceUri"]
                parts = triid.split("/")
                #print "parts=" + str(len(parts))
                trrg = azr[i]["properties"]["targetResourceUri"].split(
                    "/")[4].replace(".", "-").lower()
                trty = azr[i]["properties"]["targetResourceUri"].split(
                    "/")[6].replace(".", "-")
                trid = azr[i]["properties"]["targetResourceUri"].split(
                    "/")[8].replace(".", "-")
                # assume trty = Microsoft.Compute
                tftyp = "azurerm_virtual_machine_scale_set"
                if trty == "Microsoft-Web":
                    tftyp = "azurerm_app_service_plan"
                # case sensitite so use actual ID
                fr.write('target_resource_id = "' + triid + '"\n')
                #fr.write('target_resource_id = "${'+ tftyp + '.' + trrg + '__' + trid+'.id}"\n')
            except KeyError:
                pass

    #  profiles block
            try:
                profs = azr[i]["properties"]["profiles"]
                icount = len(profs)
                if icount > 0:
                    for j in range(0, icount):
                        fr.write('profile {\n')
                        pn = azr[i]["properties"]["profiles"][j]["name"]
                        pn = pn.replace('"', '\\"')
                        # pn="dummy"
                        # pn=pn.replace('{','\{')
                        cdef = azr[i]["properties"]["profiles"][j]["capacity"]["default"]
                        cmin = azr[i]["properties"]["profiles"][j]["capacity"]["minimum"]
                        cmax = azr[i]["properties"]["profiles"][j]["capacity"]["maximum"]
                        fr.write('\tname =  "'+pn + '"\n')
        # capacity
                        fr.write('\tcapacity {\n')
                        fr.write('\t\tdefault = "' + cdef + '"\n')
                        fr.write('\t\tminimum = "' + cmin + '"\n')
                        fr.write('\t\tmaximum = "' + cmax + '"\n')
                        fr.write('\t}\n')
        # fixed date

                        try:
                            fd = azr[i]["properties"]["profiles"][j]["fixedDate"]["end"]
                            fdend = azr[i]["properties"]["profiles"][j]["fixedDate"]["end"]
                            fdstart = azr[i]["properties"]["profiles"][j]["fixedDate"]["start"]
                            fdtz = azr[i]["properties"]["profiles"][j]["fixedDate"]["timeZone"]
                            fdend2 = fdend.split("+")[0]
                            fdstart2 = fdstart.split("+")[0]
                            fr.write('\tfixed_date {\n')
                            fr.write('\t\ttimezone =  "' + fdtz + '"\n')
                            fr.write('\t\tstart = "' + fdstart2 + '"\n')
                            fr.write('\t\tend = "' + fdend2 + '"\n')
                            fr.write('\t}\n')
                        except KeyError:
                            pass

        # recurance

                        try:
                            rec = azr[i]["properties"]["profiles"][j]["recurrence"]
                            rfr = azr[i]["properties"]["profiles"][j]["recurrence"]["frequency"]
                            # dns=str(ast.literal_eval(json.dumps(azr[i]["properties"]["dhcpOptions"]["dnsServers"])))
                            # dns=dns.replace("'",'"')

                            rsd = str(ast.literal_eval(json.dumps(
                                azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["days"])))
                            rsd = rsd.replace("'", '"')
                            rsh = str(ast.literal_eval(json.dumps(
                                azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["hours"])))
                            rsh = rsh.replace("'", '"')
                            rsm = str(ast.literal_eval(json.dumps(
                                azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["minutes"])))
                            rsm = rsm.replace("'", '"')
                            rst = azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["timeZone"]
                            fr.write('\trecurrence {\n')
                            fr.write('\t\ttimezone = "' + rst + '"\n')
                            fr.write('\t\tdays =  ' + rsd + '\n')
                            fr.write('\t\thours =  ' + rsh + '\n')
                            fr.write('\t\tminutes =  ' + rsm + '\n')
                            fr.write('\t}\n')
                        except KeyError:
                            pass

        # rules block
                        try:
                            rules = azr[i]["properties"]["profiles"][j]["rules"]
                            kcount = len(rules)
                            #print "count of rules= "+str(kcount)
                            for k in range(0, kcount):
                                #print k
                                fr.write('\trule  {\n')
                                # metric trigger
                                mtn = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["metricName"]
                                if mtn == "CPU":
                                    mtn = "Percentage CPU"

                                mtid = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["metricResourceUri"]
                                mtrrg = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["metricResourceUri"].split(
                                    "/")[4].replace(".", "-").lower()
                                mtrid = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["metricResourceUri"].split(
                                    "/")[8].replace(".", "-")
                                mtop = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["operator"]
                                mtstat = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["statistic"]
                                mtthres = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["threshold"]
                                mtta = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["timeAggregation"]
                                mttg = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["timeGrain"]
                                mttw = azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["timeWindow"]
                                mttg2 = mttg
                                mttw2 = mttw
                                #print mtthres
                                # mttg2= mttg.split(":")[1].replace("0","") # sed 's/^0*//'
                                # mttw2= mttw.split(":")[1].replace("0","") #| cut -f2 -d':' | sed 's/^0*//'

                                # metric trigger block
                                fr.write('\t\tmetric_trigger {\n')
                                fr.write('\t\t\tmetric_name = "' + mtn + '"\n')
                                fr.write(
                                    '\t\t\tmetric_resource_id = "${'+tftyp + '.' + mtrrg + '__' + mtrid + '.id}"\n')
                                fr.write('\t\t\toperator = "' + mtop + '"\n')
                                fr.write('\t\t\tstatistic= "' + mtstat + '"\n')
                                fr.write('\t\t\tthreshold = "' +
                                        str(mtthres) + '"\n')
                                fr.write(
                                    '\t\t\ttime_aggregation = "' + mtta + '"\n')
                                fr.write('\t\t\ttime_grain = "' + mttg2 + '"\n')
                                fr.write('\t\t\ttime_window = "' + mttw2 + '"\n')
                                fr.write('\t\t}\n')

                                # scale action block
                                sac = azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["cooldown"]
                                sad = azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["direction"]
                                sat = azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["type"]
                                sav = azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["value"]

                                fr.write('\t\tscale_action  {\n')
                                #print sac
                                # sac2= sac.split(":")[1].replace("0","") #| cut -f2 -d':' | sed 's/^0*//'
                                sac2 = sac
                                fr.write('\t\t\tcooldown = "' + sac2 + '"\n')
                                fr.write('\t\t\tdirection = "' + sad + '"\n')
                                fr.write('\t\t\ttype = "' + sat + '"\n')
                                fr.write('\t\t\tvalue = "' + sav + '"\n')
                                fr.write('\t\t}\n')

                                fr.write('\t}\n')  # end rule
                        except KeyError:
                            pass

                        fr.write('}\n')  # end profile
            except KeyError:
                pass
# notification block
            try:
                nots = azr[i]["properties"]["notifications"]
                ncount = len(nots)
                #print "num notifications=" + str(ncount)
                for k in range(0, ncount):
                    #print "k="+str(k)
                    nsa = azr[i]["properties"]["notifications"][k]["email"]["sendToSubscriptionAdministrator"]
                    #print "nsa "+str(nsa)
                    nsca = azr[i]["properties"]["notifications"][k]["email"]["sendToSubscriptionCoAdministrators"]
                    #print "nsca "+str(nsca)
                    nce = str(ast.literal_eval(json.dumps(azr[i]["properties"]["notifications"][k]["email"]["customEmails"])))
                    nce = nce.replace("'", '"')
                    #print "nce= "+str(nce)
                    fr.write('notification {\n')
                    fr.write('\temail {\n')

                    
                    fr.write('\t\tsend_to_subscription_administrator = ' + str(nsa).lower() + '\n')

                    
                    fr.write('\t\tsend_to_subscription_co_administrator =  ' + str(nsca).lower() + '\n')

                    fr.write('\t\tcustom_emails =   '+nce+'\n')
                    fr.write('\t}\n')
                    nwh = str(ast.literal_eval(json.dumps(
                        azr[i]["properties"]["notifications"][k]["webhooks"])))
                    nwh = nwh.replace("'", '"')
                    #fr.write('webhook =   '+nwh + '\n')
                    fr.write('}\n')
            
            except Exception as e: print(e)

                #pass

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
