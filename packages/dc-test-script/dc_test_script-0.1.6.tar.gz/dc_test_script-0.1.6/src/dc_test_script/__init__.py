import subprocess


def main():
    subprocess.run("/Users/danika/temp/test-script/src/dc_test_script/test-script.sh",
                   shell=True, executable='/bin/bash')
