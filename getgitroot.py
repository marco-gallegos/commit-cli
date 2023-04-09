import pygit2
import os

def get_git_root():
    try:
        repo = pygit2.Repository('.')
    # for now catch any error is good enough
    except:
        return None
    
    git_root = repo.workdir
    if git_root is not None and os.path.isdir(git_root):
        return git_root
    else:
        return None

if __name__ == "__main__":
    print(get_git_root())
