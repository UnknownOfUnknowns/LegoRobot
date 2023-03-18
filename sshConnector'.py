import paramiko

command = "df"
username = "root"
password = "maker"
host = "172.20.10.3"

client = paramiko.client.SSHClient()

client.connect(host, username=username, password=password)
_stdin, _stdout,_stderr = client.exec_command("df")
print(_stdout.read().decode())
client.close()
