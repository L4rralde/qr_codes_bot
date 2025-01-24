"""
Miscelaneous code
"""
import subprocess


with subprocess.Popen(
    ['git', 'rev-parse', '--show-toplevel'],
    stdout=subprocess.PIPE
) as p:
    GIT_ROOT = p.communicate()[0].rstrip().decode('utf-8')
