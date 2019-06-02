runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
bt=get_automation_runas_token()
sub=str(runas_connection["SubscriptionId"])
headers = {'Authorization': 'Bearer ' + bt, 'Content-Type': 'application/json'}
