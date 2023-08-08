import pygit2

def get_first_commit_id(repo_path):
    # Abrir el repositorio
    repo = pygit2.Repository(repo_path)

    # Obtener el primer commit
    first_commit = next(repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL))

    # Devolver el ID del primer commit como un string hexadecimal
    return first_commit.id.hex
