import json
import os

class Settings():
    def __init__(self):
        self.AltPath = None  # "data/walkers.mp4" "data/two_people.jpg"
        self.Process = True
        self.ForceAlt = False
        self.DrawFrame = False
        self.DrawMask = False
        self.DrawMoustacheDiagnostics = False
        self.DrawMoustache = True
        self.AnimationPerUpdate = 2
        self.MissingCycles = 3
        self.ImageScale = 1.0
        self.ToleranceScale = 1.0

    def user_defined_attribute(self, a):
        return not a.startswith('__') and not callable(getattr(self, a))

    def to_dict(self):
        return {a : getattr(self, a) for a in dir(self) if self.user_defined_attribute(a)}

    def to_json(self, path):
        with open(path, 'w') as outfile:
            json.dump(self.to_dict(), outfile)

    @staticmethod
    def from_json(path):

        if os.path.exists(path):
            with open(path) as json_file:
                data = json.load(json_file)
                return Settings.from_dict(data)
        else:
            return Settings()

    @staticmethod
    def from_dict(dic):
        settings = Settings()
        for k, v in dic.items():
            setattr(settings, k, v)
        return settings


