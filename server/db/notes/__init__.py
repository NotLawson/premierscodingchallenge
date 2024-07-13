## Notes DB

import json, pickle, os
from ..helpers import _internalDB, Object
class db(_internalDB):
    def __init__(self):
        super().__init__(os.path.dirname(__file__)+"/dbfile")