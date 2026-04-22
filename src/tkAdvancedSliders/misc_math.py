# Misc Math
# A collection of functions that will try to use numpy if it is installed,
# otherwise will use a pure python implementation

from .common_typing import Numeric

# Only expose the functions we have explicitly defined 
__all__ = ['linspace', 'arange']

# linspace
try:
    from numpy import linspace as np_lin  # ty:ignore[unresolved-import]
    # We wrap linspace here so the function definition is the same.
    def linspace(start: Numeric, stop: Numeric, num_steps: int) -> list[float]:
        return np_lin(start, stop, num_steps).tolist()

except ImportError:
    # https://gist.github.com/davebiagioni/1ac21feb1c2db04be4e6
    # https://stackoverflow.com/questions/60695284/linearly-spaced-array-in-c
    def linspace(start: Numeric, stop: Numeric, num_steps: int) -> list[float]:
        step = (stop - start) / (num_steps - 1)
        return [round(start + (i * step), 8) for i in range(0, num_steps)]


# arange
try:
    from numpy import arange as np_arange # ty:ignore[unresolved-import]

    def arange(
            start: Numeric, 
            stop: Numeric | None = None, 
            step: Numeric = 1
        ) -> tuple[Numeric, ...]:
        
        return tuple(np_arange(start, stop, step))

except ImportError:
    # Google Search AI gave me this, seems fine enough 
    def arange(
            start: Numeric, 
            stop: Numeric | None = None, 
            step: Numeric = 1
        ) -> tuple[Numeric, ...]:

        # Handle optional 'stop' argument like np.arange(stop)
        if stop is None:
            stop = start
            start = 0
        
        result: list[Numeric] = []
        current = start
        
        # Positive step: increment until current >= stop
        if step > 0:
            while current < stop:
                result.append(current)
                current += step

        # Negative step: decrement until current <= stop
        elif step < 0:
            while current > stop:
                result.append(current)
                current += step

        # Step of 0 is not allowed in NumPy
        else:
            raise ValueError("Step must be non-zero")
            
        return tuple(result)