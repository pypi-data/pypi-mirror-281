from gitpyapi import Git
import argparse
import os as _os
from gitpyapi import url as _url

def main():
    parser = argparse.ArgumentParser(prog='gitpyapi', usage='gitpyapi [options]', description='A Python Git Module and Script')
    subparsers = parser.add_subparsers(dest='command', help='Sub-Commands', required=True, title='Sub-Commands')
    
    # Subparser für 'clone'
    clone_parser = subparsers.add_parser('clone', help='Clone a Git Repository')
    clone_parser.add_argument('-u', '--url', type=str, help='The URL of the Git Repository', required=True)
    clone_parser.add_argument('-p', '--path', type=str, help='The Path of the Git Repository', required=True)
    
    # Subparser für 'add'
    add_parser = subparsers.add_parser('add', help='Add a File to the Git Repository')
    add_parser.add_argument('-f', '--file', type=str, help='The File to add to the Git Repository', required=True)
    
    # Subparser für 'commit'
    commit_parser = subparsers.add_parser('commit', help='Commit Changes to Git')
    commit_parser.add_argument('-m', '--message', type=str, help='The Message of the Commit', required=True)
    
    # Subparser für 'push'
    push_parser = subparsers.add_parser('push', help='Push Changes to Git')
    push_parser.add_argument('-b', '--branch', type=str, help='The Branch of the Git Repository')
    push_parser.add_argument('-r', '--remote', type=str, help='The Remote of the Git Repository')
    
    args = parser.parse_args()
    cmd = args.command
    
    if cmd == 'clone':
        url = args.url
        path = args.path
        if not _os.path.exists(path):
            _os.makedirs(path, exist_ok=True)
        name = _url(url)
        endpath = _os.path.join(path, name)
        git = Git(url=url, path=endpath)
        git.clone()
    elif cmd == 'add':
        url = args.url
        path = args.path
        git = Git(url=url, path=path)
        git.add(file_path=args.file)
    elif cmd == 'commit':
        url = args.url
        path = args.path
        git = Git(url=url, path=path)
        git.commit(message=args.message)
    elif cmd == 'push':
        url = args.url
        path = args.path
        remote = args.remote if args.remote else 'default'
        branch = args.branch if args.branch else 'master'
        git = Git(url=url, path=path, remote_name=remote, branch=branch)
        git.push()
    else:
        print(f'Unknown command: {cmd}')

if __name__ == '__main__':
    main()