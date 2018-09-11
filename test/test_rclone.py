import subprocess, os

def test_version():
    subprocess.check_call(['rclone', '--version'])

def test_simple_clone(tmpdir):
    repo = os.path.join(tmpdir.strpath, 'repo')
    subprocess.check_call(['rclone', 'https://github.com/pfultz2/rclone', repo])

def test_simple_clone_branch(tmpdir):
    repo = os.path.join(tmpdir.strpath, 'repo')
    subprocess.check_call(['rclone', '-b', 'master', 'https://github.com/pfultz2/rclone', repo])

def test_simple_clone_branch_hash(tmpdir):
    repo = os.path.join(tmpdir.strpath, 'repo')
    subprocess.check_call(['rclone', '-b', 'master', '-c', '55ae38271f7dd95664dbc9fd2a476c40be5dc551', 'https://github.com/pfultz2/rclone', repo])

def test_recursive_clone(tmpdir):
    repo = os.path.join(tmpdir.strpath, 'repo')
    subprocess.check_call(['rclone', 'https://github.com/RadeonOpenCompute/hcc.git', repo])
    print os.listdir(os.path.join(repo, 'clang'))
    assert os.path.exists(os.path.join(repo, 'clang', 'CMakeLists.txt'))



