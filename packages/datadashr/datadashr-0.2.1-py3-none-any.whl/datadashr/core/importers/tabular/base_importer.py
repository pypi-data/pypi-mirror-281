class BaseImporter:
    def __init__(self, connector):
        self.connector = connector

    def import_data(self, source, table_name, filters, reset):
        raise NotImplementedError("import_data method must be implemented by subclasses")
