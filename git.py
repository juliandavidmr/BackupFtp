import subprocess
import os


class cd:
    """
    Context manager for changing the current working directory
    https://stackoverflow.com/a/13197763/5125608
    """

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def execute(cmd):
    """
    Execute command
    https://stackoverflow.com/a/95246/5125608
    """
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def doctor(dirfolder):
    print "Running doctor analysis...\n"

    gitfolder = os.path.join(dirfolder, ".git")

    # Check folder .git
    if not os.path.exists(gitfolder):
        msg = "[ERROR]\t" + gitfolder + " not exits"
        print msg
        raise Exception(msg)
    else:
        print "[OK]\t", gitfolder, "exits"


def commit(dirfolder, msg):
    doctor(dirfolder)

    # enter the directory like this:
    with cd(dirfolder):
        # List files
        p = execute("ls")
        FILES = p.stdout.readlines()
        COUNTF = len(FILES)
        print "[WARN]\t", COUNTF, "items found into", dirfolder, "folder"

        # git add .
        p = execute(["git", "add", "."])

        # git status
        p = execute(["git", "status"])
        for line in p.stdout.readlines():
            line = str(line)
            if "new file" in line or "modified" in line:
                print "[GIT]\tgit status OK",
                break

        # count files changed
        # p = execute("git whatchanged -1 --format=oneline | wc -l".split(" "))
        # print p.stdout.readlines()
        # print "\n[GIT]\t", len(p.stdout.readlines()), "files modified"

        # git commit -m ""
        p = execute("git commit -m".split(" ") + ["\"" + str(msg) + "\""])
        print "[GIT]\t", "Commit", ''.join(p.stdout.readlines())

        # git push
        print "[WARN]\tUploading files to git"
        p = execute("git push -u origin master")
        print "[GIT]\t", "Push", ''.join(p.stdout.readlines())

