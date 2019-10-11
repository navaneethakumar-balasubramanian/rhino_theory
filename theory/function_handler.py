from scipy.optimize import curve_fit
from boltons.funcutils import FunctionBuilder
from functools import partial
import pickle
import numpy as np

class ModelingFunction:
    def __init__(self, equation,
                 variables=['x', 'y', 'z'],
                 constants=['a','b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w'],
                 name='equation',
                ):
        self.equation = equation
        self.name = name
        self.constants = [c for c in constants if c in equation]
        self.variables = [c for c in variables if c in equation]
        self._fitted = False

    def __call__(self, X, *args):
        X = np.asarray(X)
        if self._fitted:
            return self.as_partial(X)
        else:
            return self.as_function(X, *args)

    @property
    def as_function(self):
        fb = FunctionBuilder(name=self.name,
                             body='import numpy as np\nreturn ' + self.equation,
                             args=self.variables + self.constants)
        return fb.get_func()

    @property
    def as_partial(self):
        if self._fitted:
            return partial(self.as_function, **dict(list(zip(self.as_function.__code__.co_varnames, np.r_[None, self.optimals]))[1:]))
        else:
            return self.as_function

    def fit(self, X, y):
        self._fitted = True
        self.optimals, _ = curve_fit(self.as_function, X, y, maxfev=1000000)

    def predict(self, X):
        X = np.asarray(X)
        return self.as_function(X, *self.optimals)

    def get_fitted_string(self):
        if self._fitted:
            equation = self.equation
            for const, opt in zip(self.constants, self.optimals):
                equation = equation.replace(const, str(opt))
            return equation
        else:
            return self.equation

    def __repr__(self):
        return '<Equation: {} - Curve Fitted: {}>'.format(self.equation, self._fitted)

    def save(self, filename):
        pickle.dump(self, open(filename, 'wb'))

    @classmethod
    def load(self, filename):
        return pickle.load(open(filename, 'rb'))
