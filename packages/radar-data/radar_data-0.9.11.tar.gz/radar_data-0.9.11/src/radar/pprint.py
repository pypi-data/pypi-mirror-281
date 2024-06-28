import pprint
import numpy as np


class NumpyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, obj, context, maxlevels, level):
        if isinstance(obj, np.ndarray):
            return np.array2string(obj, separator=", ", suppress_small=True), True, False
        return super().format(obj, context, maxlevels, level)


pp = NumpyPrettyPrinter(indent=1, depth=2, width=140, sort_dicts=False)


def pprint(obj):
    pp.pprint(obj)
