# Dummy-Module für vereinfachte Installation ohne externe Abhängigkeiten

class SQLAlchemy:
    class declarative_base:
        def __init__(self, *args, **kwargs):
            pass

    class Column:
        def __init__(self, *args, **kwargs):
            self.type = kwargs.get('type', 'String')
            self.primary_key = kwargs.get('primary_key', False)

    class Integer: Column:
        def __init__(self, *args, **kwargs):
            pass

    class String: Column:
        def __init__(self, *args, **kwargs):
            pass

    class DateTime: Column:
        def __init__(self, *args, **kwargs):
            pass

    class Float: Column:
        def __init__(self, *args, **kwargs):
            pass

    class Boolean: Column:
        def __init__(self, *args, **kwargs):
            pass

    class ForeignKey:
        def __init__(self, *args, **kwargs):
            pass

    class relationship:
        def __init__(self, *args, **kwargs):
            self.back_populates = kwargs.get('back_populates', None)

class Column:
    def __init__(self, *args, **kwargs):
        pass

class relationship:
    def __init__(self, *args, **kwargs):
        self.back_populates = kwargs.get('back_populates', None)

class declarative_base:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        class Model:
            pass
        return Model()

class ForeignKey:
    def __init__(self, *args, **kwargs):
        pass

def declarative_base_func(*args, **kwargs):
    return declarative_base()
