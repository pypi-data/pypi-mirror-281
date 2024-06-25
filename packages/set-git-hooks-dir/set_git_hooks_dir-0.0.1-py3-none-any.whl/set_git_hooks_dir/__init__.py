import os
import os.path as path
import subprocess
import sys
import site
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        super().run()
        try:
            setup('.git-hooks')
        except Exception as exc:
            print(exc, file=sys.stderr)

def _find_dot_git(dirpath: str) -> str:
    site_packages = site.getsitepackages()

    for candidate in site_packages:
        cur = cwd
        while True:
            hooks_dir = path.join(cur, dirpath)
            dot_git = path.join(cur, '.git')
            if path.isdir(hooks_dir) and path.exists(dot_git):
                return dot_git
            parent = path.dirname(cur)
            if parent == cur:
                break
            cur = parent

    raise Exception(f'Git hooks directory {dirpath} was not found at any root of GitHub repository in {site_packages}')

def setup(dirpath: str) -> None:
    for name in ['SET_GIT_HOOKS_DIR_SKIP', 'GITHUB_ACTION', 'CI', 'JENKINS_URL']:
        if os.getenv(name):
            return

    dirpath = path.normpath(dirpath)
    dot_git = _find_dot_git(dirpath)
    if path.isdir(dot_git):
        with open(path.join(dot_git, 'config'), encoding='utf-8') as file:
            for line in file:
                if line.startswith('\thooksPath = '):
                    return  # core.hooksPath is already configured. Skip

    git = os.getenv('SET_GIT_HOOKS_DIR_GIT') or 'git'
    result = subprocess.run([git, 'config', 'core.hooksPath', dirpath], encoding='utf-8', cwd=path.dirname(dot_git))
    if result.returncode != 0:
        raise Exception(f'`{git} config core.hooksPath {dir} failed with status {result.returncode}: {result.stderr}')
