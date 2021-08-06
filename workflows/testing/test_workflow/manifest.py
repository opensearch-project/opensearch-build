import yaml

class BundleManifest:
    @staticmethod
    def from_file(path):
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
            return BundleManifest(data)

    @staticmethod
    def from_text(text):
        data = yaml.safe_load(text)
        return BundleManifest(data)

    def __init__(self, data):
        schema_version = str(data['schema-version'])
        if schema_version != '1.0':
            raise ValueError(f'Schema version must be 1.0; found {schema_version}')
        self._build_id = data['build']['build-id']
        self._bundle_location = data['build']['location']
        self._components = list(map(lambda entry: Component(entry), data['components']))

    def build_id(self):
        return self._build_id

    def bundle_location(self):
        return self._bundle_location

    def components(self):
        return self._components

class Component:
    def __init__(self, data):
        self._name = data['name']
        self._repository = data['repository']
        self._commit = data['commit']

    def name(self):
        return self._name

    def repository_url(self):
        return self._repository

    def commit_id(self):
        return self._commit
