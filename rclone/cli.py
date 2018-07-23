import subprocess, click

from rclone import __version__

@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=__version__, prog_name='rclone')
@click.option('-b', '--branch')
@click.argument('url', required=True)
@click.argument('path', required=False)
def cli(branch, url, path):
    clone_cmd = ['git', 'clone', '--depth', '1']
    if branch: clone_cmd.extend(['-b', branch])
    if url: clone_cmd.extend([url])
    if path: clone_cmd.extend([path])
    subprocess.check_call(clone_cmd)

