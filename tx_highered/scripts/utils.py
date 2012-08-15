from lxml import html as etree


class DictReader(object):
    fieldnames = None
    mapping = None

    def __init__(self, filehandle, **kwargs):
        doc = etree.parse(filehandle)
        # TODO better header detection
        # TODO know when to stop
        rows = doc.xpath('//tr')

        self.rows = rows

        if 'fieldnames' in kwargs:
            self.fieldnames = kwargs['fieldnames']
        else:
            fieldnames = [x.text_content().strip() for x in rows[0].getchildren()]
            self.fieldnames = fieldnames

        if 'mapping' in kwargs:
            self.mapping = kwargs['mapping']

    def normalize_keys(self, data):
        if self.mapping is None:
            return data
        for key in data.keys():
            if key in self.mapping:
                value = data.pop(key)
                data[self.mapping[key]] = value

    def __iter__(self):
        return self.readrow_as_dict()

    def readrow_as_dict(self):
        for row in self.rows[1:]:
            data = dict(zip(self.fieldnames, [x.text_content().strip() for x in row.getchildren()]))
            self.normalize_keys(data)
            yield data
