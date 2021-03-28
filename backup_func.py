def backup_func():

    """
    Recursively backup all the files in a remote directory
    """

    # information about the source sftp server
    # and directories

    hostname = 'ip'
    port = 22 #default port for ssh/sftp is 22, change if needed
    username = 'user'
    password = 'password'
    start_directory = 'dir to backup'
    backup_dir = 'dir to save to (on local machine, same that the bot is running on)'

    import paramiko
    import os
    import datetime
    import discord
    from discord.ext import commands

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


    def backup_directory(local_dir, remote_dir):
        os.chdir(local_dir)
        sftp.chdir(remote_dir)
        print(('In directory ' + remote_dir))

        files, directories = get_files_directories()

        for f in files:
            print(('Backing up ' + f))
            try:
                sftp.get(f, f)
            except PermissionError:
                print(('Skipping ' + f + ' due to permissions'))

        for d in directories:
            newremote = remote_dir + d + '/'
            newlocal = local_dir + '\\' + d
            os.mkdir(newlocal)
            backup_directory(newlocal, newremote)


    # Main program

    # backup directories under here

    os.chdir(backup_dir)

    # Create directory with today's date

    datestring = str(datetime.date.today())

    os.mkdir(datestring)
    os.chdir(datestring)
    local_dir = os.getcwd()

    # connect to sftp server

    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # back up everthing from top directory

    remote_dir = start_directory

    backup_directory(local_dir, remote_dir)

    # quit sftp connection

    sftp.close()
    transport.close()
