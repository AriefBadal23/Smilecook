TRAP_ARTISTS =[
    'Ricky Ross',
    'Future',
    'Desiigner',
    'Young Jeezy'
]


class TrapArtist():
    def __init__(self, name):
        self.name = name
   
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name not in TRAP_ARTISTS:
            raise ValueError(f'{name} is not a trap artist')
        self._name = name


rr = TrapArtist('Rick Ross')
print(rr.name)
rr.name = 'Ricky Rose'
print(rr.name)
