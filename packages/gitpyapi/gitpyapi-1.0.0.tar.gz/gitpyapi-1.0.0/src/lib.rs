use pyo3::prelude::*; /// Basis Einbindung fuer pyo3
use git2::{Repository, Signature, PushOptions, RemoteCallbacks}; /// Einbindung fuer git2-rs, Repository und andere notwendige Strukturen
use pyo3::exceptions::PyException; /// Basis Exception, brauche ich fuer meine eigenen Exceptions.
use pyo3::create_exception; /// Zum erstellen eigener Exception Klassen.

/// Nun ist es soweit, am besten Fangen wir mit einer Basis Exception fuer all Unsere anderen Exceptions an.
create_exception!(gitpyapi /* Wird Gebraucht da ich angeben muss, zu welchem Modul meine Exception gehoert */, GitPyApiBaseError /* Der Name der Basis Exception Klasse */, PyException /* Hier binde ich die Basis Exception Klasse ein. */); /// Alles muss mit einem Semikolon Enden

#[pyfunction]
fn clone(url: &str, path: &str) -> PyResult<()> {
    match Repository::clone(url, path) {
        Ok(repo) => {
            println!("Repository cloned to {}", repo.path().display());
            Ok(())
        },
        Err(e) => {
            println!("Error cloning repository: {}", e);
            Err(GitPyApiBaseError::new_err(e.to_string()))
        }
    }
}

#[pyfunction]
fn add(repo_path: &str, file_path: &str) -> PyResult<()> {
    let repo = Repository::open(repo_path).map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    let mut index = repo.index().map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    index.add_path(std::path::Path::new(file_path)).map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    index.write().map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    Ok(())
}

#[pyfunction]
fn commit(repo_path: &str, message: &str, author: &str, email: &str) -> PyResult<()> {
    let repo = Repository::open(repo_path).map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    let mut index = repo.index().map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    let tree_id = index.write_tree().map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    let tree = repo.find_tree(tree_id).map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    let sig = Signature::now(author, email).map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    let parent_commit = repo.head().map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?.peel_to_commit().map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    repo.commit(Some("HEAD"), &sig, &sig, message, &tree, &[&parent_commit]).map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    Ok(())
}

#[pyfunction]
fn push(repo_path: &str, remote_name: &str, branch: &str) -> PyResult<()> {
    let repo = Repository::open(repo_path).map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    let mut remote = repo.find_remote(remote_name).map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    let mut push_options = PushOptions::new();
    let mut callbacks = RemoteCallbacks::new();
    callbacks.credentials(|_url, _username_from_url, _allowed_types| {
        git2::Cred::ssh_key_from_agent("git")
    });
    push_options.remote_callbacks(callbacks);
    remote.push(&[&format!("refs/heads/{}", branch)], Some(&mut push_options)).map_err(|e| GitPyApiBaseError::new_err(e.to_string()))?;
    Ok(())
}

/// Das Python Modul, wo ich alles zusammen baue.
#[pymodule]
fn gitpyapi(m: &PyModule) -> PyResult<()> {
    /// Damit wir die Exception verwenden koennen, muessen wir sie dem Modul Hinzufuegen, das machen wir folgendermassen
    m.add("GitPyApiBaseError", m.py().get_type::<GitPyApiBaseError>())?; /// Hiermit haben wir die Exception Erfolgreich Hinzugefuegt.
    m.add_function(wrap_pyfunction!(clone, m)?)?; /// Hier haben wir die Funktion Erfolgreich Hinzugefuegt.
    m.add_function(wrap_pyfunction!(add, m)?)?; /// Hier haben wir die Funktion Erfolgreich Hinzugefuegt.
    m.add_function(wrap_pyfunction!(commit, m)?)?; /// Hier haben wir die Funktion Erfolgreich Hinzugefuegt.
    m.add_function(wrap_pyfunction!(push, m)?)?; /// Hier haben wir die Funktion Erfolgreich Hinzugefuegt.
    Ok(())
}