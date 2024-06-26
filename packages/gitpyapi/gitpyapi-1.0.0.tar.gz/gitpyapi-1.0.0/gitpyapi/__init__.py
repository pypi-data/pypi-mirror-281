"""
GitPyApi, Python Git Client Module, written in Rust and Python.
(c) 2024 Kevin Alexander Krefting, pyrootcpp, pacflypy, Germany, Wuppertal.
Language: Python 3(.12)
Maintainer: Kevin Alexander Krefting.
"""
# Rust implementierte Module haben oft das Problem, dass sie nur in der Interaktiven shell geshen werden koennen,
# Aber nicht von IDE's, zwar lassen sie sich nutzen, werden aber nicht gezeigt.
# Zudem sind oftmals Rust Module etwas Unflexibler als Python Module, daher bauen wir hier Wrapper Funktionen,
# Die die Rust Funktionen aufrufen und um Docstrings und Felexibilitaeten erweitern.
# Das Modul wird mit pyo3 erstellt.

from .gitpyapi import GitPyApiBaseError as _gpabe # Wir Binden die Exception GitPyApiBaseError versehen im aber eine Privaten Alias, damit man es nicht ausserhalb erkennt.
import os as _os # Hier Importieren wir das Os modul und machen es Privat

__all__ = [] # Wir erstellen eine Leere Liste, damit die IDE's wissen, welche Funktionen und Klassen von außen zugänglich sein sollen.

class GitPyApiBaseError(_gpabe): # Hier erstellen wir die Basis Exception beim Original Namen, und erben vom Original, das tun wir damit wir einen wrapper schlagen koennen.
    """
    GitPyApiBaseError is an Base Exception for all Exceptions in GitPyApi.
    """
    def __init__(self, *args): # Hier erstellen wir die Funktion die direkt mit der Klasse aufgerufen wird
        """
        Initial the Exception and Pass Arguments to the Exception.
        """
        super().__init__(*args) # Hier rufen wir die Original Exception auf und passen die Argumente zu ihm, so koennen wir die Exception in der IDE sehen, ohne dass die Funktion sich je geandert hat.
        self.args = args # Hier speichern wir die Argumente, die die Exception bekommt.
        self.message = " ".join(args) # Hier erstellen wir die Nachricht, die die Exception wirft.

__all__.append('GitPyApiBaseError') # Hier fgen wir die Exception zur Liste der zugänglich sein sollen Funktionen hinzu.

class Git: # Wir erstellen die Klasse git, welches die Entsprechenden Funktionen aus dem Rust Modul aufruft.
    """
    Class to Work with Git.
    """
    def __init__(self, url: str, path: str = 'default', repo_path: str = None, branch: str = 'master', remote_name: str = 'origin'): # Hier erstellen wir die Funktion die direkt mit der Klasse aufgerufen wird
        """
        Initial the Git Class and Pass Arguments to the Class.
        """
        import urllib.parse as _parse
        if path == 'default':
            _resp = _parse.urlparse(url)
            _path = _resp.path
            _name = _os.path.basename(_path)
            _path2 = _os.getcwd()
            _path3 = _os.path.join(_path2, _name)
            self.path = _path3
        else:
            self.path = path # Hier speichern wir den Pfad, der die Exception bekommt.
        self.url = url # Hier speichern wir die URL, die die Exception bekommt.
        self.repo_path = repo_path # Hier speichern wir den Pfad, der die Exception bekommt.
        self.branch = branch # Hier speichern wir den Pfad, der die Exception bekommt.
        self.remote_name = remote_name # Hier speichern wir den Pfad, der die Exception bekommt.

    def clone(self):
        """
        Clone the Repository to the Given Path.
        """
        from .gitpyapi import clone as _clone # Wir Importieren die Funktion extra im Modul damit man diese Nicht ausserhalb siet und Machen den Namen privat um konflikte zu vermeiden.
        _clone(url=self.url, path=self.path) # Hier rufen wir die Funktion auf und passen die Argumente zu ihm.

    def add(self, file_path: str = 'default'):
        """
        Add the File to the Repository.
        """
        from .gitpyapi import add as _add # Wir Importieren die Funktion extra im Modul damit man diese Nicht ausserhalb siet und Machen den Namen privat um konflikte zu vermeiden.
        if self.repo_path is None:
            raise GitPyApiBaseError('Repo Path is None, Please Set the Repo Path First.')
        if file_path == 'default':
            file_path = self.repo_path
        _add(repo_path=self.repo_path, file_path=file_path) # Hier rufen wir die Funktion auf und passen die Argumente zu ihm.

    def commit(self, message: str = 'update', author: str = 'anonym', author_email: str = 'anonym@example.com'):
        """
        Commit Changes to Git.
        """
        from .gitpyapi import commit as _commit # Wir Importieren die Funktion extra im Modul damit man diese Nicht ausserhalb siet und Machen den Namen privat um konflikte zu vermeiden.
        if self.repo_path is None:
            raise GitPyApiBaseError('Repo Path is None, Please Set the Repo Path First.')
        _commit(repo_path=self.repo_path, message=message, author=author, email=author_email) # Hier rufen wir die Funktion auf und passen die Argumente zu ihm.

    def push(self):
        """
        Push the Changes to Git.
        """
        from .gitpyapi import push as _push # Wir Importieren die Funktion extra im Modul damit man diese Nicht ausserhalb siet und Machen den Namen privat um konflikte zu vermeiden.
        if self.repo_path is None:
            raise GitPyApiBaseError('Repo Path is None, Please Set the Repo Path First.')
        _push(repo_path=self.repo_path, remote_name=self.remote_name, branch=self.branch) # Hier rufen wir die Funktion auf und passen die Argumente zu ihm.

__all__.append('Git') # Hier fgen wir die Klasse zur Liste der zugänglich sein sollen Funktionen hinzu.

def url(url: str) -> str:
    """
    Convert the URL to a valid URL.
    """
    import urllib.parse as _parse
    _parsed = _parse.urlparse(url)
    _path = _parsed.path
    return _os.path.basename(_path)

__all__.append('url') # Hier fgen wir die Funktion zur Liste der zugänglich sein sollen Funktionen hinzu.