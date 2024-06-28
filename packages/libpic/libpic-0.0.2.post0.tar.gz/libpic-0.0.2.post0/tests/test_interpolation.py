import unittest
from time import perf_counter_ns

import numpy as np
from scipy.constants import c, e
from libpic.current.cpu import current_deposit_2d

from libpic.interpolation.interpolation_2d import interpolation_2d


class TestCurrentDeposition(unittest.TestCase):

    def test_numba_func(self):
        npart = 1
        x = np.array([1])
        y = np.array([1])
        ex_part = np.empty((1,))
        ey_part = np.empty((1,))
        ez_part = np.empty((1,))
        bx_part = np.empty((1,))
        by_part = np.empty((1,))
        bz_part = np.empty((1,))

        nx = 3
        ny = 3
        x0 = 0.0
        y0 = 0.0
        dx = 1.0
        dy = 1.0
        
        ex = np.arange(nx*ny, dtype='f8').reshape((nx, ny))
        ey = ex
        ez = np.zeros((nx, ny))
        bx = np.zeros((nx, ny))
        by = np.zeros((nx, ny))
        bz = np.zeros((nx, ny))
        pruned = np.array([False])
        
        interpolation_2d(
            x, y, ex_part, ey_part, ez_part, bx_part, by_part, bz_part, npart,
            ex, ey, ez, bx, by, bz,
            dx, dy, x0, y0,
            pruned,
        )
        print(ex, ex_part)
        print(ey, ey_part)

        