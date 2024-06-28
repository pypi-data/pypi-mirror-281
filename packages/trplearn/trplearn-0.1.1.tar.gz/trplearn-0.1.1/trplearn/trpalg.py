import numpy as np

from abc import ABC, abstractmethod

class TropicalAlgebra(ABC):
    """
    Tropical algebra abstract base class.
    """
    @abstractmethod
    def __init__(self, data):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def add(self, other):
        pass

    @abstractmethod
    def dualadd(self, other):
        pass

    @abstractmethod
    def mult(self, other):
        pass
    
    @abstractmethod
    def dualmult(self, other):
        pass

    @abstractmethod
    def dot(self, other):
        pass

    @abstractmethod
    def dualdot(self, other):
        pass

    @abstractmethod
    def pow(self, n):
        pass

    @abstractmethod
    def dualpow(self, n):
        pass

    @property
    @abstractmethod
    def C(self):
        pass

    @property
    @abstractmethod
    def H(self):
        pass

class Manipulation:
    """
    Basic common manipulation for TropicalAlgebra classes.
    """
    def __init__(self, data):
        self.data = np.array(data)

    @property
    def T(self):
        """
        Getting the transposed array.
        """
        return self.__class__(self.data.T)
    
    @property
    def ndim(self):
        """
        Number of array dimensions.
        """
        return self.data.ndim
    
    def to_numpy(self):
        """
        Convert to the numpy array.
        """
        return self.data
    
    def to_list(self):
        """
        Convert to the python native list.
        """
        return self.data.tolist()
    
class MaxPlus(TropicalAlgebra, Manipulation):
    """Max-plus double semiring.
    
    Max-plus double semiring is the following algebraic system: :math:`(\double{R}\cup{\pm\infty},-\infty,0,\max,+, +\infty,0,\min,+,-a)`,
    where set, zero, unit, add, mult, dualzero, dualunit, dualadd, dualmult, conjugate, from left to right.

    Parameters
    ----------
    data : array-like
        An array.
    """
    def __init__(self, data):
        Manipulation.__init__(self, data)

    def __repr__(self):
        data_str = np.array2string(self.data, max_line_width=np.inf).replace('\n', '\n        ')
        return f"MaxPlus({data_str})"

    def __add__(self, other):
        return self.add(other)
    
    def __sub__(self, other):
        return self.dualadd(other)

    def __mul__(self, other):
        return self.mult(other)
    
    def __truediv__(self, other):
        return self.dualmult(other)

    def __matmul__(self, other):
        return self.dot(other)

    def __pow__(self, n):
        return self.pow(n)
        
    def add(self, other):
        """
        Max-plus addition defined by :math:`a\oplus b=\max(a,b)`.

        Parameters
        ----------
        other : int, float, MaxPlus
            Addition.

        Returns
        -------
        MaxPlus
            Result of max-plus addition by other.

        Examples
        --------
        >>> a = MaxPlus(3)
        >>> b = MaxPlus(5)
        >>> a.add(b)
        MaxPlus(5)

        >>> c = MaxPlus([1, 5, 3])
        >>> d = MaxPlus([4, 2, 6])
        >>> c.add(d)
        MaxPlus([4 5 6])

        >>> A = MaxPlus([[1, 3], [5, 7]])
        >>> B = MaxPlus([[2, 6], [4, 8]])
        >>> A.add(B)
        MaxPlus([[2 6]
                 [5 8]])
        """
        if isinstance(other, (int, float)):
            other = MaxPlus([other])
        elif not isinstance(other, MaxPlus):
            return NotImplemented

        return MaxPlus(np.maximum(self.data, other.data))
    
    def dualadd(self, other):
        """
        Max-plus dual-addition defined by :math:`a\ominus b=\min(a,b)`.

        Parameters
        ----------
        other : int, float, MaxPlus
            Dual-addition.

        Returns
        -------
        MaxPlus
            Result of max-plus dual-addition by other.
        """
        if isinstance(other, (int, float)):
            other = MaxPlus([other])
        elif not isinstance(other, MaxPlus):
            return NotImplemented

        return MaxPlus(np.minimum(self.data, other.data))
    
    def mult(self, other):
        """
        Max-plus multiplication defined by :math:`a\otimes b=a+b`.

        Parameters
        ----------
        other : int, float, MaxPlus
            Multiplication.

        Returns
        -------
        MaxPlus
            Result of max-plus multiplication by other.
        """
        if isinstance(other, (int, float)):
            other = MaxPlus([other])
        elif not isinstance(other, MaxPlus):
            return NotImplemented

        return MaxPlus(self.data + other.data)
    
    def dualmult(self, other):
        """
        Max-plus dual-multiplication (same as multiplication).

        Parameters
        ----------
        other : int, float, MaxPlus
            Dual-multiplication.

        Returns
        -------
        MaxPlus
            Result of max-plus dual-multiplication by other.
        """
        return self.mult(other)
        
    def dot(self, other):
        """
        Max-plus matrix multiplication.

        Parameters
        ----------
        other : MaxPlus
            The matrix to multiply with.

        Returns
        -------
        MaxPlus
            Result of max-plus matrix multiplication.
        """
        if isinstance(other, (int, float)):
            other = MaxPlus([other])
        elif not isinstance(other, MaxPlus):
            return NotImplemented

        if self.data.ndim <= 1 or other.data.ndim <= 1:
            return NotImplemented

        result = np.zeros((self.data.shape[0], other.data.shape[1]))
        for i in range(self.data.shape[0]):
            for j in range(other.data.shape[1]):
                result[i, j] = np.max(self.data[i, :] + other.data[:, j])

        return MaxPlus(result)
    
    def dualdot(self, other):
        """
        Max-plus dual matrix multiplication.

        Parameters
        ----------
        other : MaxPlus
            The matrix to multiply with.

        Returns
        -------
        MaxPlus
            Result of max-plus dual matrix multiplication.
        """
        if isinstance(other, (int, float)):
            other = MaxPlus([other])
        elif not isinstance(other, MaxPlus):
            return NotImplemented

        if self.data.ndim <= 1 or other.data.ndim <= 1:
            return NotImplemented

        result = np.zeros((self.data.shape[0], other.data.shape[1]))
        for i in range(self.data.shape[0]):
            for j in range(other.data.shape[1]):
                result[i, j] = np.min(self.data[i, :] + other.data[:, j])

        return MaxPlus(result)

    def pow(self, n):
        """
        Max-plus matrix power.

        Parameters
        ----------
        n : int
            The power to raise the matrix to.

        Returns
        -------
        MaxPlus
            Result of max-plus matrix power.

        Raises
        ------
        ValueError
            If n is negative.
        """
        if n < 0:
            raise ValueError("Negative exponents are not supported for MaxPlus algebra.")
        elif n == 0:
            result = np.ones_like(self.data) * (-np.inf)
            for i in range(len(self.data)):
                result[i, i] = 0
            return MaxPlus(result)
        elif n == 1:
            return self
        else:
            result = self
            for _ in range(n - 1):
                result = result @ self
            return result
    
    def dualpow(self, n):
        """
        Max-plus dual matrix power.

        Parameters
        ----------
        n : int
            The power to raise the matrix to.

        Returns
        -------
        MaxPlus
            Result of max-plus dual matrix power.

        Raises
        ------
        ValueError
            If n is negative.
        """
        if n < 0:
            raise ValueError("Negative exponents are not supported for MaxPlus algebra.")
        elif n == 0:
            result = np.ones_like(self.data) * (np.inf)
            for i in range(len(self.data)):
                result[i, i] = 0
            return MaxPlus(result)
        elif n == 1:
            return self
        else:
            result = self
            for _ in range(n - 1):
                result = result.dualdot(self)
            return result
        
    @property
    def C(self):
        """
        Getting the conjugation array.

        Returns
        -------
        MaxPlus
            The conjugate of the current MaxPlus object.
        """
        return MaxPlus(-self.data)
    
    @property
    def H(self):
        """
        Getting the Hermitian array.

        Returns
        -------
        MaxPlus
            The Hermitian of the current MaxPlus object.
        """
        return self.T.C
    
class MinPlus(TropicalAlgebra, Manipulation):
    """Min-plus double semiring.
    
    Min-plus double semiring is the following algebraic system: :math:`(\double{R}\cup{\pm\infty},+\infty,0,\min,+, -\infty,0,\max,+,-a)`,
    where set, zero, unit, add, mult, dualzero, dualunit, dualadd, dualmult, conjugate, from left to right.

    Parameters
    ----------
    data : array-like
        An array.
    """
    def __init__(self, data):
        Manipulation.__init__(self, data)

    def __repr__(self):
        data_str = np.array2string(self.data, max_line_width=np.inf).replace('\n', '\n        ')
        return f"MinPlus({data_str})"
    
    def __add__(self, other):
        return self.add(other)
    
    def __sub__(self, other):
        return self.dualadd(other)

    def __mul__(self, other):
        return self.mult(other)
    
    def __truediv__(self, other):
        return self.dualmult(other)

    def __matmul__(self, other):
        return self.dot(other)

    def __pow__(self, n):
        return self.pow(n)
    
    def add(self, other):
        """
        Min-plus addition defined by :math:`a\oplus b=\min(a,b)`.

        Parameters
        ----------
        other : int, float, MinPlus
            Addition.

        Returns
        -------
        MinPlus
            Result of min-plus addition by other.

        Examples
        --------
        >>> a = MinPlus(3)
        >>> b = MinPlus(5)
        >>> a.add(b)
        MinPlus(3)

        >>> c = MinPlus([1, 5, 3])
        >>> d = MinPlus([4, 2, 6])
        >>> c.add(d)
        MinPlus([1 2 3])

        >>> A = MinPlus([[1, 3], [5, 7]])
        >>> B = MinPlus([[2, 6], [4, 8]])
        >>> A.add(B)
        MinPlus([[1 3]
                 [4 7]])
        """
        if isinstance(other, (int, float)):
            other = MinPlus([other])
        elif not isinstance(other, MinPlus):
            return NotImplemented

        return MinPlus(np.minimum(self.data, other.data))
    
    def dualadd(self, other):
        """
        Min-plus dual-addition defined by :math:`a\ominus b=\max(a,b)`.

        Parameters
        ----------
        other : int, float, MinPlus
            Dual-addition.

        Returns
        -------
        MinPlus
            Result of min-plus dual-addition by other.
        """
        if isinstance(other, (int, float)):
            other = MinPlus([other])
        elif not isinstance(other, MinPlus):
            return NotImplemented

        return MinPlus(np.maximum(self.data, other.data))
    
    def mult(self, other):
        """
        Min-plus multiplication defined by :math:`a\otimes b=a+b`.

        Parameters
        ----------
        other : int, float, MinPlus
            Multiplication.

        Returns
        -------
        MinPlus
            Result of min-plus multiplication by other.
        """
        if isinstance(other, (int, float)):
            other = MinPlus([other])
        elif not isinstance(other, MinPlus):
            return NotImplemented

        return MinPlus(self.data + other.data)
    
    def dualmult(self, other):
        """
        Min-plus dual-multiplication (same as multiplication).

        Parameters
        ----------
        other : int, float, MinPlus
            Dual-multiplication.

        Returns
        -------
        MinPlus
            Result of min-plus dual-multiplication by other.
        """
        return self.mult(other)
        
    def dot(self, other):
        """
        Min-plus matrix multiplication.

        Parameters
        ----------
        other : MinPlus
            The matrix to multiply with.

        Returns
        -------
        MinPlus
            Result of min-plus matrix multiplication.
        """
        if isinstance(other, (int, float)):
            other = MinPlus([other])
        elif not isinstance(other, MinPlus):
            return NotImplemented

        if self.data.ndim <= 1 or other.data.ndim <= 1:
            return NotImplemented

        result = np.zeros((self.data.shape[0], other.data.shape[1]))
        for i in range(self.data.shape[0]):
            for j in range(other.data.shape[1]):
                result[i, j] = np.min(self.data[i, :] + other.data[:, j])

        return MinPlus(result)
    
    def dualdot(self, other):
        """
        Min-plus dual matrix multiplication.

        Parameters
        ----------
        other : MinPlus
            The matrix to multiply with.

        Returns
        -------
        MinPlus
            Result of min-plus dual matrix multiplication.
        """
        if isinstance(other, (int, float)):
            other = MinPlus([other])
        elif not isinstance(other, MinPlus):
            return NotImplemented

        if self.data.ndim <= 1 or other.data.ndim <= 1:
            return NotImplemented

        result = np.zeros((self.data.shape[0], other.data.shape[1]))
        for i in range(self.data.shape[0]):
            for j in range(other.data.shape[1]):
                result[i, j] = np.max(self.data[i, :] + other.data[:, j])

        return MinPlus(result)
    
    def pow(self, n):
        """
        Min-plus matrix power.

        Parameters
        ----------
        n : int
            The power to raise the matrix to.

        Returns
        -------
        MinPlus
            Result of min-plus matrix power.

        Raises
        ------
        ValueError
            If n is negative.
        """
        if n < 0:
            raise ValueError("Negative exponents are not supported for MinPlus algebra.")
        elif n == 0:
            result = np.ones_like(self.data) * (np.inf)
            for i in range(len(self.data)):
                result[i, i] = 0
            return MinPlus(result)
        elif n == 1:
            return self
        else:
            result = self
            for _ in range(n - 1):
                result = result @ self
            return result
    
    def dualpow(self, n):
        """
        Min-plus dual matrix power.

        Parameters
        ----------
        n : int
            The power to raise the matrix to.

        Returns
        -------
        MinPlus
            Result of min-plus dual matrix power.

        Raises
        ------
        ValueError
            If n is negative.
        """
        if n < 0:
            raise ValueError("Negative exponents are not supported for MinPlus algebra.")
        elif n == 0:
            result = np.ones_like(self.data) * (-np.inf)
            for i in range(len(self.data)):
                result[i, i] = 0
            return MinPlus(result)
        elif n == 1:
            return self
        else:
            result = self
            for _ in range(n - 1):
                result = result.dualdot(self)
            return result
        
    @property
    def C(self):
        """
        Getting the conjugation array.

        Returns
        -------
        MinPlus
            The conjugate of the current MinPlus object.
        """
        return MinPlus(-self.data)
    
    @property
    def H(self):
        """
        Getting the Hermitian array.

        Returns
        -------
        MinPlus
            The Hermitian of the current MinPlus object.
        """
        return self.T.C