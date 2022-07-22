



class Message(object):

    def __init__(self, texte, gras=False, retourLigne=False, couleur=[0, 0, 0, 0.16]):
        self._gras=gras
        self._couleur=couleur
        self._texte=texte
        self._needRetourLigne=retourLigne



    @property
    def gras(self):
        return self._gras

        

    @property
    def couleur(self):
        return self._couleur

        

    @property
    def texte(self):
        return self._texte


    @property
    def needRetourLigne(self):
        return self._needRetourLigne

        

    @gras.setter
    def gras(self, gras):
        self._gras=gras

        

    @couleur.setter
    def couleur(self, couleur):
        self._couleur=couleur

        

    @texte.setter
    def texte(self, texte):
        self._texte=texte

    def __add__(self, message):
        if isinstance(message, Message):
            self._texte=self._texte+message.texte
        elif isinstance(message, str):
            self._texte=self._texte+message

        

    def __str__(self):
        return self._texte















