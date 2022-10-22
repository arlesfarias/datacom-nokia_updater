from paramiko import SSHClient, AutoAddPolicy
import re


class Olt:

    def __init__(self, ip, port, usr, pwd) -> None:
        self.ip = ip
        self.port = port
        self.usr = usr
        self.pwd = pwd
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(self.ip, self.port, self.usr,
                         self.pwd, timeout=5)

    def get_onu_by_serial(self, serial):
        if re.match(r"^ALCL[0-9A-F]{8}$", serial):
            cmd = f"show interface gpon onu | include {serial}"
            _, content, __ = self.ssh.exec_command(cmd)
            content = content.read().decode("utf-8").split()
        else:
            return None, None
        try:
            port = content[0]
            onu_id = content[1]
            print(f"ONT {serial} encontrada: {port} {onu_id}")
            return port, onu_id
        except:
            print(f"ONT {serial} não encontrada!")
            return None, None

    def upgrade_onu(self, port, onu_id):
        cmd = f"request firmware onu install ALC.bin interface gpon" + \
            f" {port} onu {onu_id}"
        print(f"Executando comando: {cmd}")
        _, content, __ = self.ssh.exec_command(cmd)
        content = content.read().decode("utf-8")
        print(content)
        return cmd
