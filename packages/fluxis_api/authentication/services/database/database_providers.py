

DATABASE_PROVIDERS = {
    'postgresql': 'Postgresql',
    'sqlite': 'SQLite',
    'mysql': 'MySQL',
}

DATABASE_PROVIDERS_CHOICE = [(key, name)
                             for (key, name) in DATABASE_PROVIDERS.items()]
