class ElasticObject:
    def __init__(self, **kwargs):
        self._attributes = {}
        self._setup_attributes(**kwargs)

    def _setup_attributes(self, **kwargs):
        for key, value in kwargs.items():
            self._attributes[key] = value

    def __getattr__(self, name):
        if name in self._attributes:
            return self._attributes[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith('_') or name.startswith('__'):
            super().__setattr__(name, value)
        else:
            if '_attributes' not in self.__dict__:
                super().__setattr__('_attributes', {})

            self._attributes[name] = value

    def __repr__(self):
        return f'{self.__class__.__name__}({self._attributes})'
