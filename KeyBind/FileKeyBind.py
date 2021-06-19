from KeyBind import KeyBind

class FileKeyBind(KeyBind):
    def __init__(self, key = "", name = "", page = "", contents = ()):
        KeyBind.__init__(self, key, name, page, contents)


    def GetKeyBindString(self):

        payload = '$$'.join([i for i in self.Contents if i])

        return f'{self.Key} "{payload}"\n'


