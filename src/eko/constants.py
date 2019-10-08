"""
    This files sets the physical constants of the code.

    Upon initialization it will set all constants and won't allow further changes.
    Done in this way to allow for future extension to config files or other different choices.
"""

from eko import t_float

class Constants:
    """
    Upon initialization all constants are set and a `lock` variable is put is place.
    As long as the `lock` variable is active, setting attributes of this class will result
    in an attributeError exception.

    Attributes
    ----------
      NC: int
        Number of colors = 3

      TF: t_float
        normalization of fundamental generators = 1/2

      CA : f_float
        second Casimir constant in adjoint representation = NC

      CF : f_float
        second Casimir constant in fundamental representation = (NC^2 - 1)/(2 NC)

    """
    _lock = False
    def __init__(self):
        self.NC = 3
        self.TF = t_float(1./2.)
        self.CA = t_float(self.NC)
        self.CF = t_float((self.NC*self.NC - 1.)/(2. * self.NC))
        # Lock the class
        self.lock = True

    @property
    def lock(self):
        return self._lock
    @lock.setter
    def lock(self, value):
        self.__dict__["_lock"] = value # Set like this otherwise lock locks the lock

    def __setattr__(self, name, value):
        if self.lock:
            raise AttributeError("Modifying the Constants class is not allowed")
        super().__setattr__(name, value)

    def dict(self):
        """ Returns the constants class in the form of a dictionary.
        In practicse: returns the __dict__ attribute of the class without the
        protected variables

        Returns
        -------
        out_dict: dictionary
            dictionary with the attributes of the class
        """
        out_dict = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return out_dict

    def __str__(self):
        return str(self.dict())
