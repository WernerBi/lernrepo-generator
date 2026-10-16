"""Positive artifact lists bind release inputs to the current course build."""
from .build import assert_build_current, build_fingerprint
from .io import file_hash, read, write


def index(course, directory, files):
    assert_build_current(course)
    value = {'fingerprint': build_fingerprint(course),
             'files': {path.relative_to(course.root).as_posix(): file_hash(path) for path in files}}
    write(directory / 'artifact-index.json', value)
    return value


def listed(course, directory):
    value = read(directory / 'artifact-index.json')
    if not value:
        return []
    if value.get('fingerprint') != build_fingerprint(course):
        raise ValueError(f'Veralteter Export: {directory.name}; erneut erzeugen')
    paths = []
    for name, fingerprint in value['files'].items():
        path = course.local(name)
        if not path.is_file() or file_hash(path) != fingerprint:
            raise ValueError(f'Export verändert oder fehlt: {name}')
        paths.append(path)
    return paths
