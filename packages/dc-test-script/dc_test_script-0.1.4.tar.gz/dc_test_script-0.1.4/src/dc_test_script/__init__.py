import subprocess
import sys


def main():
    command = sys.argv[1:]

    print(command)

    subprocess.run("/Users/danika/temp/test-script/src/test_script/test-script.sh", shell=True, executable='/bin/bash')