import subprocess


def execution_powershell_hote_distant(server, username, password,query):
    # Créer une chaîne d'informations d'identification PowerShell
    creds_command = f"$username = '{username}'; $password = ConvertTo-SecureString '{password}' -AsPlainText -Force; $cred = New-Object System.Management.Automation.PSCredential($username, $password)"
    
    
    ps_command = f"""
    $session = New-PSSession -ComputerName {server} -Credential $cred;
    Invoke-Command -Session $session -ScriptBlock {{ {query} }};
    Remove-PSSession -Session $session
    """

    # Exécuter la commande PowerShell avec la connexion distante
    result = subprocess.run(
        ["powershell", "-Command", creds_command + ps_command],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        output = result.stdout.strip()
        # st = output[output.find("------  -------------- ----------") + len("------  -------------- ----------"):output.find(server)] 
        # print (st)
        # return st.strip()
        return output
    else:
        return ''