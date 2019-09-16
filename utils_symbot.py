#utilities for SymBot
import os, asyncio
import datetime, time


class Perm_Command:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    #getters and setters
    def set_name(self, name):
        self.name = name

    def set_content(self, content):
        self.content = content

    def get_name(self):
        return self.name

    def get_content(self):
        return self.content

class Dynamic_Command:
    def __init__(self, name, content, exp_date = None):
        self.name = name
        self.content = content
        self.exp_date = exp_date

        if exp_date == None:
            t = datetime.datetime.now()
            #adding time for it to expire
            self.exp_date = t + datetime.timedelta(days=8)


    #getters , ignoring setters since they are unnecessary
    def get_name(self):
        return self.name

    def get_content(self):
        return self.content

    def get_exp_date(self):
        return self.exp_date


class Commandmanager:
    def __init__(self):
        self.perm_commands = []
        self.dynamic_commands = []
        self.perm_commandcount = 0
        self.dynamic_commandcount = 0
        self.read_perm_commands()
        self.read_dynamic_commands()
    #getter for commandcounts (no setter beause they wouldn't make sense)
    def get_perm_commandcount(self):
        return self.perm_commandcount


# Section for dynamic commands

    def get_expire_date(self, ask):
        for cmd in self.dynamic_commands:
            if cmd.get_name() == ask:
                now = datetime.datetime.now()
                delta = cmd.get_exp_date() - now
                return delta.total_seconds()
        return None

    def check_expired(self, cmd):
        now = datetime.datetime.now()
        expire = cmd.get_exp_date() - now
        seconds = expire.total_seconds()
        if seconds < 0:
            return 0
        else:
            return seconds

    def check_commands(self):
        for cmd in self.dynamic_commands:
            time = self.check_expired(cmd)
            if time < 1:
                self.dynamic_commands.remove(cmd)


    def add_dynamic_command(self, name, content):
        cmd = Dynamic_Command(name, content)
        #checking all permanent commands
        for ecmd in self.perm_commands:
            if ecmd.get_name() == name:
                return 2
        #checking all dynamic commands, if not exists, ready to create
        if not cmd in self.dynamic_commands:
            self.dynamic_commands.append(cmd)
            self.dynamic_commandcount += 1
            return 1
        else:
            return 2

    def add_existing_dynamic_command(self, name, content, exp_date):
        cmd = Dynamic_Command(name, content, exp_date)
        if not cmd in self.perm_commands:
            if not cmd in self.dynamic_commands:
                self.dynamic_commands.append(cmd)
                self.dynamic_commandcount += 1
                return 1
            else:
                return 2
        else:
            return 2

    def read_dynamic_commands(self):
        # n will be the number of commands initialized
        n = 0
        #check if file exists, only open if it exists
        if not os.path.exists('dynamic_commands.symbot'):
            return
        else:
            cmds = open('dynamic_commands.symbot', 'r')
            for line in cmds:
                #syntax of internal command: name, comtent
                raw = line.split(' ', 2)
                #syntax for adding command: name, content, exp_date
                check = self.add_existing_dynamic_command(raw[0], raw[2], raw[1])
                if check == 1:
                    n += 1
            cmds.close()
            return n

    def save_dynamic_commands(self):
        pass


    def run_command(self, name):
        #priority 1 are permanent commands
        for cmd in self.perm_commands:
            if cmd.get_name() == name:
                return cmd.get_content()

        for cmd in self.dynamic_commands:
            if cmd.get_name() == name:
                return cmd.get_content()
        #now community commands

        return 'Command does not exist!'


    def add_perm_command(self, name, content):
        cmd = Perm_Command(name, content)
        if not cmd in self.perm_commands:
            self.perm_commands.append(cmd)
            self.perm_commandcount += 1
            return 1
        else:
            return 2

    def read_perm_commands(self):
        # n will be the number of commands initialized
        n = 0
        #check if file exists, only open if it exists
        if not os.path.exists('perm_commands.symbot'):
            return 0
        else:
            cmds = open('perm_commands.symbot', 'r')
            for line in cmds:
                #syntax of internal command: name, comtent
                raw = line.split(' ', 1)
                #syntax for appending command: name, content
                check = self.add_perm_command(raw[0], raw[1])
                if check == 1:
                    n = n+1
            cmds.close()
            return n
