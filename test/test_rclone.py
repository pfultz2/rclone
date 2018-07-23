import subprocess, os

def test_version():
    subprocess.check_call(['rclone', '--version'])

def test_simple_clone(tmpdir):
    subprocess.check_call(['rclone', 'https://github.com/pfultz2/rclone'], cwd=tmpdir.strpath)

def test_simple_clone_branch(tmpdir):
    subprocess.check_call(['rclone', '-b', 'master', 'https://github.com/pfultz2/rclone'], cwd=tmpdir.strpath)

def test_simple_clone_path(tmpdir):
    subprocess.check_call(['rclone', '-b', 'master', 'https://github.com/pfultz2/rclone', os.path.join(tmpdir.strpath, 'repo')])

