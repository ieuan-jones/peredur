from fitparse import FitFile

class Activity:
    def __init__(self, file_data=None, file_format=None):
        self.records = []

        if file_data:
            if file_format == 'fit':
                self.import_fit(file_data)

    def import_fit(self, file_data):
        FF = FitFile(file_data)

        for record in FF.get_messages('record'):
            r = {}
            for entry in record:
                r[entry.name] = entry.value
            self.records.append(r)
