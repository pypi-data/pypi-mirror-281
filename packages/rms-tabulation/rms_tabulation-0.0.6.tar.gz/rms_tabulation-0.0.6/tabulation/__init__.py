################################################################################
# tabulation.py
#
# The Tabulation class represents a function by a sequence of linear
# interpolations between points defined by arrays of x and y coordinates.
#
# Mark Showalter, PDS Rings Node, December 2011
################################################################################

from __future__ import division

import numpy as np
from scipy.interpolate import interp1d

try:
    from ._version import __version__
except ImportError as err:
    __version__ = 'Version unspecified'


class Tabulation(object):
    """A class that represents a function by a sequence of linear interpolations
    between points defined by arrays of x and y coordinates. The function is
    treated as equal to zero outside the range of the x coordinates."""

    def __init__(self, x, y):
        """Constructor for a Tabulation object.

        Input:
            x       a 1-D array of x-coordinates, which must be monotonic.
            y       a 1-D array of y-values, given in the same order as the
                    x-coordinates.
        """

        ignore = self._update(x,y)

########################################
# Private methods
########################################

    def _update(self, x, y):
        """Updates a tabulation in place with new x and y arrays."""

        x = np.asarray(x, dtype=np.double)
        y = np.asarray(y, dtype=np.double)
        sorted = np.sort(x)

        if len(x.shape) != 1:
            raise ValueError("x array is not 1-dimensional")

        if x.shape != y.shape:
            raise ValueError("x and y arrays do not have the same size")

        if np.all(sorted == x):
            self.x = x
            self.y = y
        elif np.all(sorted == x[::-1]):
            self.x = x[::-1]
            self.y = y[::-1]
        else:
            raise ValueError("x-coordinates are not monotonic")

        self.func = None
        return self

    def _update_y(self, new_y):
        """Updates a tabulation in place with a new y array."""

        y = np.asarray(new_y, dtype=np.double)

        if y.shape != self.x.shape:
            raise ValueError("x and y arrays do not have the same size")

        self.y = y
        self.func = None
        return self

    def _trim(self):
        """Updates the given Tabulation by deleting leading and trailing regions
        of the domain that contain nothing but zeros. This is never strictly
        necessary but can improve efficiency and reduce memory requirements. It
        can be useful because many filter bandpass functions contains strings of
        zeros at one end or the other.

        NOTE that this function operates in-place, returning the same
        Tabulation object.
        """

        # Trim the trailing end
        (new_x, new_y) = Tabulation._trim1(self.x[::-1], self.y[::-1])

        # Trim the leading end
        (new_x, new_y) = Tabulation._trim1(new_x[::-1], new_y[::-1])

        return self._update(new_x, new_y)

    @staticmethod
    def _trim1(x,y):
        """Private procedure used by trim() to strip away the leading end of
        an (x,y) array pair.
        """

        # Define a mask at the low end
        mask = np.cumsum(y != 0.) != 0

        # Shift left by one to keep last zero
        mask[:-1] = mask[1:]

        return (x[mask], y[mask])

    @staticmethod
    def _xmerge(x1, x2):
        """Returns a new array of x-values containing the union of x-values
        found in each of the given arrays.
        """

        # Confirm overlap
        if x1[0] > x2[-1] or x2[0] > x1[-1]:
            raise ValueError("domains do not overlap")

        # Merge and sort
        sorted = np.sort(np.hstack((x1, x2)))

        # Locate and remove duplicates
        mask = np.append(sorted[:-1] != sorted[1:], True)
        return sorted[mask]

    @staticmethod
    def _xoverlap(x1,x2):
        """Returns a new array of x-values containing the union of x-values from
        each of the given arrays that fall within the intersection of the two
        domains.
        """

        new_x = Tabulation._xmerge(x1,x2)
        mask = (new_x >= max(x1[0],x2[0])) & (new_x <= min(x1[-1],x2[-1]))
        return new_x[mask]

########################################
# Standard operators
########################################

    def __call__(self, x):
        # Fill in the 1-D interpolation if necessary
        if self.func is None:
            self.func = interp1d(self.x, self.y, kind="linear",
                                 bounds_error=False, fill_value=0.)

        if np.shape(x):
            return self.func(x)

        return float(self.func(x))

    def __mul__(self, other):

        # Multiplication of two Tabulations
        # Note: the new domain is the intersection of the given domains
        if type(other) == type(self):
            new_x = Tabulation._xoverlap(self.x, other.x)
            return Tabulation(new_x, self(new_x) * other(new_x))._trim()

        # Otherwise just scale the y-values
        elif np.shape(other) == ():
            return Tabulation(self.x, self.y * other)

        raise ValueError("Cannot multiply Tabulation by given value")

    def __truediv__(self, other):

        # Division of two Tabulations
        # Note: the new domain is the intersection of the given domains
        if type(other) == type(self):
            new_x = Tabulation._xoverlap(self.x, other.x)
            return Tabulation(new_x, self(new_x) / other(new_x))._trim()

        # Otherwise just scale the y-values
        elif np.shape(other) == ():
            return Tabulation(self.x, self.y / other)

        raise ValueError("Cannot divide Tabulation by given value")

    def __add__(self, other):

        # Addition of two Tabulations
        # Note: the new domain is the union of the given domains
        if type(other) == type(self):
            new_x = Tabulation._xmerge(self.x, other.x)
            return Tabulation(new_x, self(new_x) + other(new_x))

        # Otherwise just shift the y-values
        elif np.shape(other) == ():
            return Tabulation(self.x, self.y + other)

        raise ValueError("Cannot add Tabulation by given value")

        # Note that a constant added to a Tabulation will still return zero
        # outside the domain.

    def __sub__(self, other):

        # Subtraction of two Tabulations
        # Note: the new domain is the union of the given domains
        if type(other) == type(self):
            new_x = Tabulation._xmerge(self.x, other.x)
            return Tabulation(new_x, self(new_x) - other(new_x))

        # Otherwise just shift the y-values
        elif np.shape(other) == ():
            return Tabulation(self.x, self.y - other)

        raise ValueError("Cannot subtract Tabulation by given value")

        # Note that a constant subtracted from a Tabulation will still return
        # zero outside the domain.

    def __imul__(self, other):

        # In-place multiplication of two Tabulations
        if type(other) == type(self):
            new_x = Tabulation._xoverlap(self.x, other.x)
            return self._update(new_x, self(new_x) * other(new_x))._trim()

        # Otherwise just scale the y-values
        elif np.shape(other) == ():
            return self._update_y(self.y * other)

        raise ValueError("Cannot multiply Tabulation in-place by given value")

    def __itruediv__(self, other):

        # In-place division of two Tabulations
        if type(other) == type(self):
            new_x = Tabulation._xoverlap(self.x, other.x)
            return self._update(new_x, self(new_x) / other(new_x))._trim()

        # Otherwise just scale the y-values
        elif np.shape(other) == ():
            return self._update_y(self.y / other)

        raise ValueError("Cannot divide Tabulation in-place by given value")

    def __iadd__(self, other):

        # In-place addition of two Tabulations
        if type(other) == type(self):
            new_x = Tabulation._xmerge(self.x, other.x)
            return self._update(new_x, self(new_x) + other(new_x))

        # Otherwise just shift the y-values
        elif np.shape(other) == ():
            return self._update_y(self.y + other)

        # Note that a constant added to a Tabulation will still return zero
        # outside the domain.

        raise ValueError("Cannot add Tabulation in-place by given value")

    def __isub__(self, other):

        # In-place subtraction of two Tabulations
        if type(other) == type(self):
            new_x = Tabulation._xmerge(self.x, other.x)
            return self._update(new_x, self(new_x) - other(new_x))

        # Otherwise just shift the y-values
        elif np.shape(other) == ():
            return self._update_y(self.y - other)

        # Note that a constant subtracted from a Tabulation will still return
        # zero outside the domain.
        raise ValueError("Cannot subtract Tabulation in-place by given value")

########################################
# Additional methods
########################################

    def trim(self):
        """Returns a new Tabulation (shallow copy) in which the zero-valued
        leading and trailing regions of the domain have been removed."""

        # Save the original arrays
        x = self.x
        y = self.y

        # Create a trimmed version
        self._trim()        # operates in-place
        result = Tabulation(self.x, self.y)

        # Restore the original
        self.x = x
        self.y = y

        return result

    def domain(self):
        """Returns a tuple containing the range of x-values over which the
        function is nonzero.
        """

        return (self.x[0], self.x[-1])

    def clip(self, xmin, xmax):
        """Returns a tuple in which the domain has been redefined as
        (xmin,xmax).
        """

        new_x = Tabulation._xmerge(self.x, np.array((xmin,xmax)))
        mask = (new_x >= xmin) & (new_x <= xmax)
        return self.resample(new_x[mask])

    def locate(self, yvalue):
        """Returns a list of the x-values where the Tabulation has the given
        value of y. Note that the exact ends of the domain are not checked."""

        signs = np.sign(self.y - yvalue)
        mask = (signs[:-1] * signs[1:]) < 0.

        xlo = self.x[:-1][mask]
        ylo = self.y[:-1][mask]

        xhi = self.x[1:][mask]
        yhi = self.y[1:][mask]

        xarray = xlo + (yvalue - ylo)/(yhi - ylo) * (xhi - xlo)
        xlist = list(xarray) + list(self.x[signs == 0])
        xlist.sort()

        return xlist

    def integral(self):
        """Returns the integral of [y dx].
        """

        # Make an array consisting of the midpoints between the x-values
        # Begin with an array holding one extra element
        dx = np.empty(self.x.size + 1)

        dx[1:] = self.x         # Load the array shifted right
        dx[0]  = self.x[0]      # Replicate the endpoint

        dx[:-1] += self.x       # Add the array shifted left
        dx[-1]  += self.x[-1]

        # dx[] is now actually 2x the value at each midpoint.

        # The weight on each value is the distance between the adjacent midpoints
        dx[:-1] -= dx[1:]   # Subtract the midpoints shifted right (not left)

        # dx[] is now actually -2x the correct value of each weight. The last
        # element is to be ignored.

        # The integral is now the sum of the products y * dx
        return -0.5 * np.sum(self.y * dx[:-1])

    def resample(self, new_x):
        """Re-samples a tabulation at a given list of x-values."""

        if new_x is None:
            # If new_x is None, return a copy of the current tabulation
            return Tabulation(self.x, self.y.copy())

        return Tabulation(new_x, self(new_x))

    def subsample(self, new_x):
        """Resamples a tabulation at the given list of x-values, while at the
        same time retaining all original x-values."""

        new_x = Tabulation._xmerge(new_x, self.x)
        return Tabulation(new_x, self(new_x))

    def mean(self, dx=None):
        """Returns the mean value of the tabulation. If specified, dx is the
        minimum step permitted along the x-axis during integration."""

        trimmed = self.trim()

        if dx is None:
            resampled = Tabulation(self.x, self.y.copy())
                                            # y cannot be a shallow copy...
        else:
            (x0,x1) = trimmed.domain()
            new_x = np.arange(x0 + dx, x1, dx).astype("float")
            resampled = trimmed.subsample(new_x)

        integ0 = resampled.integral()

        resampled.y *= resampled.x          # ...because we change y in-place
        integ1 = resampled.integral()

        return integ1/integ0

    def bandwidth_rms(self, dx=None):
        """Returns the root-mean-square width of the tabulation. This is the
        mean value of (y * (x - x_mean)**2)**(1/2). If specified, dx is the
        minimum step permitted along the x-axis during integration."""

        trimmed = self.trim()

        if dx is None:
            resampled = Tabulation(self.x, self.y.copy())
                                            # y cannot be a shallow copy...
        else:
            (x0,x1) = trimmed.domain()
            new_x = np.arange(x0 + dx, x1, dx).astype("float")
            resampled = trimmed.subsample(new_x)

        integ0 = resampled.integral()

        resampled.y *= resampled.x          # ...because we change y in-place
        integ1 = resampled.integral()

        resampled.y *= resampled.x          # ...twice!
        integ2 = resampled.integral()

        return np.sqrt(((integ2*integ0 - integ1**2) / integ0**2))

    def pivot_mean(self, precision=0.01):
        """Returns the "pivot" mean value of the tabulation. The pivot value is
        the mean value of y(x) d(log(x)). Note all x must be positive."""

        trimmed = self.trim()
        (x0,x1) = trimmed.domain()

        log_x0 = np.log(x0)
        log_x1 = np.log(x1)
        log_dx = np.log(1. + precision)

        new_x = np.exp(np.arange(log_x0, log_x1 + log_dx, log_dx))

        resampled = trimmed.subsample(new_x)
        integ1 = resampled.integral()

        resampled.y /= resampled.x
        integ0 = resampled.integral()

        return integ1/integ0

    def fwhm(self, fraction=0.5):
        max = np.max(self.y)
        limits = self.locate(max * fraction)
        assert len(limits) == 2
        return limits[1] - limits[0]

    def square_width(self):
        return self.integral() / np.max(self.y)
