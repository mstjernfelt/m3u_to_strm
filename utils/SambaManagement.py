from smb.SMBConnection import SMBConnection

class SambaManagement:
    share_user_name = ""
    share_password = ""
    remote_name = ""
    remote_share = ""
    domain = ""
    connection = ""
    connected = ""

    def __init__(self, userName, password, remotename, remoteshare, domain):
        self.share_user_name = userName
        self.share_password = password
        self.remote_name = remotename
        self.remote_name = remoteshare
        self.domain = domain

        self.connection = SMBConnection(self.share_user_name,self.share_password,'client',self.remote_name, domain="MrNas") 
        self.connected = self.conn.connect(self.remote_name,445)

    def create_dir(self, new_folder_name):
        try:

            try:
                self.createDirectory(self.remote_share, new_folder_name)
            except Exception as e:
                print(f'### can not create folder: {e}')    
        except Exception as e:
            print(f'### can not access the system: {e}')

        self.connected.close()