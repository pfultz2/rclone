import subprocess, click, tarfile, urllib, os, exceptions, ConfigParser, StringIO, tempfile

from rclone import __version__

def extract_ar(archive, dst, **kwargs):
    # TODO: Delete directory
    d = tempfile.mkdtemp()
    tarfile.open(archive, **kwargs).extractall(d)
    f = os.path.join(d, os.listdir(d)[0])
    os.rename(f, dst)

class RCloneURLOpener(urllib.FancyURLopener):
    def http_error_default(self, url, fp, errcode, errmsg, headers):
        if errcode >= 400:
            raise exceptions.RuntimeError("Download failed with error {0} for: {1}".format(errcode, url))
        return urllib.FancyURLopener.http_error_default(self, url, fp, errcode, errmsg, headers)

def download(url, filename):
    RCloneURLOpener().retrieve(url, filename=filename)
    return filename
        
class Submodule:
    def __init__(self, repo, name, url, path, commit):
        self.repo = repo
        self.name = name
        self.url = url
        self.path = path
        self.commit = commit

    def fetch(self):
        if 'github.com' in self.url:
            start = self.url.find('github.com')+len('github.com/')
            gh = self.url[start:].replace('.git', '')
            f = os.path.join(self.repo, self.name+'.tar.gz')
            download('https://github.com/{}/archive/{}.tar.gz'.format(gh, self.commit), f)
            extract_ar(f, self.path, mode='r:gz')
            os.remove(f)
        else:
            subprocess.check_call(['git', 'clone', self.url, self.path])
            subprocess.check_call(['git', 'checkout', self.commit], cwd=self.path)

# Strip the config file of whitespaces
def stripfile(f):
    return StringIO.StringIO('\n'.join((line.strip() for line in open(f).readlines())))

def get_submodules(repo):
    commits = {}
    for line in subprocess.check_output(['git', 'submodule'], cwd=repo).splitlines():
        words = line.split()
        commit = words[0].strip('-')
        path = words[1]
        commits[path] = commit
    if len(commits) > 0:
        config = ConfigParser.ConfigParser(allow_no_value=True)
        config.readfp(stripfile(os.path.join(repo, '.gitmodules')))
        for section in config.sections():
            if section.startswith('submodule "'):
                name = section[11:-1]
                url = config.get(section, 'url')
                path = config.get(section, 'path')
                fullpath = os.path.join(repo, path)
                commit = commits[path]
                yield Submodule(repo, name, url, fullpath, commit)


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=__version__, prog_name='rclone')
@click.option('-b', '--branch')
@click.option('-c', '--commit')
@click.argument('url', required=True)
@click.argument('path', required=True)
def cli(branch, commit, url, path):
    clone_cmd = ['git', 'clone']
    if branch: clone_cmd.extend(['-b', branch])
    if not commit: clone_cmd.extend(['--depth', '1'])
    subprocess.check_call(clone_cmd+[url, path])
    if commit:
        subprocess.check_call(['git', 'checkout', commit], cwd=path)
    for m in get_submodules(path):
        m.fetch()


