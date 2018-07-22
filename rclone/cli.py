import subprocess, click

from rclone import __version__

@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=__version__, prog_name='rclone')
@click.argument('url')
def cli(url):
    subprocess.check_call('git clone --depth 1 {url}'.format(url=url))

