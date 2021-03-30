
# IMPORTS #
import datetime
import os
import paramiko


def backup_func(info: dict, from_dir: str, to_dir: str):

    """
    Recursively backup all the files in a remote directory
    """

    def get_files_directories():
        file_list = sftp.listdir('.')

        files = []
        directories = []

        for file_name in file_list:
            try:
                stat = str(sftp.lstat(file_name))
                if stat[0] == 'd':
                    directories.append(file_name)
                elif stat[0] == '-':
                    files.append(file_name)
            except PermissionError:
                print(('Skipping ' + file_name + ' due to permissions'))

        return files, directories

    def backup_directory(local, remote):
        """
        Copy the files in "remote" directory to "local" directory
        """
        os.chdir(local)
        sftp.chdir(remote)
        print(('In directory ' + remote))

        files, directories = get_files_directories()

        for f in files:
            print(('Backing up ' + f))
            try:
                sftp.get(f, f)
            except PermissionError:
                print(('Skipping ' + f + ' due to permissions'))

        for d in directories:
            new_remote = remote + d + '/'
            new_local = local + '\\' + d
            os.mkdir(new_local)
            backup_directory(new_local, new_remote)

    # MAIN PROGRAM #
    # Creating directory
    os.chdir(to_dir)  # Changing working directory to to_dir
    date_string = str(datetime.date.today())  # Getting today's date
    os.mkdir(date_string)  # Create directory with today's date
    os.chdir(date_string)  # Changing directory to it
    local_dir = os.getcwd()  # Getting directory path of the current working directory

    # Connecting to SFTP server
    transport = paramiko.Transport((info["hostname"], info["port"]))  # Creating SSH session
    transport.connect(username=info["username"], password=info["password"])  # Connecting to user
    sftp = paramiko.SFTPClient.from_transport(transport)  # Creating SFTP client channel

    # Copying files from from_dir to to_dir
    remote_dir = from_dir  # Creating variable named remote_dir to avoid confusion
    backup_directory(local_dir, remote_dir)  # Copy files

    # Cleaning up
    sftp.close()  # Closing SFTP client channel
    transport.close()  # Closing SSH session

    return True
