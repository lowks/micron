class Template:
    def __init__(self, tfile, **kwargs):
        self.tfile = tfile
        self.kwargs = kwargs


def template(tfile, **data):
    return Template(tfile, **data)
