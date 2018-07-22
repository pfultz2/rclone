import subprocess

def test_version():
    subprocess.check_call(['rclone', '--version'])

