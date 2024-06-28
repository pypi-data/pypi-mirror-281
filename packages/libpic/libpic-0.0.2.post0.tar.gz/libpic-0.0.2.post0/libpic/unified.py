
# import numpy as np
# from numba import njit, prange
# from scipy.constants import c

# from .current.cpu import calculate_S
# from .interpolation.interpolation_2d import *
# from .pusher.boris import boris_cpu

# # from llvmlite.binding import set_option
# # set_option('', "-force-vector-width=2")


# @njit(inline="always")
# def interp(x, y, dx, dy, x0, y0, ex, ey, ez, bx, by, bz):

#     gx = np.zeros(3)
#     gy = np.zeros(3)
#     hx = np.zeros(3)
#     hy = np.zeros(3)

#     x_over_dx = (x - x0) / dx
#     y_over_dy = (y - y0) / dy

#     ix1 = int(np.floor(x_over_dx+0.5))
#     get_gx(ix1 - x_over_dx, gx)

#     ix2 = int(np.floor(x_over_dx))
#     get_gx(ix2 - x_over_dx + 0.5, hx)

#     iy1 = int(np.floor(y_over_dy+0.5))
#     get_gx(iy1 - y_over_dy, gy)

#     iy2 = int(np.floor(y_over_dy))
#     get_gx(iy2 - y_over_dy + 0.5, hy)

#     return interp_ex(ex, hx, gy, ix2, iy1), interp_ey(ey, gx, hy, ix1, iy2), interp_ez(ez, gx, gy, ix1, iy1), \
#            interp_bx(bx, gx, hy, ix1, iy2), interp_by(by, hx, gy, ix2, iy1), interp_bz(bz, hx, hy, ix2, iy2)


# @njit(inline="always")
# def project(x, y, ux, uy, uz, inv_gamma, w, dx, dy, dt, q, jx, jy, jz, rho):
#     S0x = np.zeros(5)
#     S1x = np.zeros(5)
#     S0y = np.zeros(5)
#     S1y = np.zeros(5)
#     DSx = np.zeros(5)
#     DSy = np.zeros(5)
#     jy_buff = np.zeros(5)

#     vx = ux*c*inv_gamma
#     vy = uy*c*inv_gamma
#     vz = uz*c*inv_gamma
#     x_old = x - vx*0.5*dt
#     y_old = y - vy*0.5*dt
#     x_adv = x + vx*0.5*dt
#     y_adv = y + vy*0.5*dt

#     # positions at t + dt/2, before pusher
#     # +0.5 for cell-centered coordinate
#     x_over_dx0 = x_old / dx
#     ix0 = int(np.floor(x_over_dx0+0.5))
#     y_over_dy0 = y_old / dy
#     iy0 = int(np.floor(y_over_dy0+0.5))

#     calculate_S(x_over_dx0 - ix0, 0, S0x)
#     calculate_S(y_over_dy0 - iy0, 0, S0y)

#     # positions at t + 3/2*dt, after pusher
#     x_over_dx1 = x_adv / dx
#     ix1 = int(np.floor(x_over_dx1+0.5))
#     dcell_x = ix1 - ix0

#     y_over_dy1 = y_adv / dy
#     iy1 = int(np.floor(y_over_dy1+0.5))
#     dcell_y = iy1 - iy0

#     calculate_S(x_over_dx1 - ix1, dcell_x, S1x)
#     calculate_S(y_over_dy1 - iy1, dcell_y, S1y)

#     for i in range(5):
#         DSx[i] = S1x[i] - S0x[i]
#         DSy[i] = S1y[i] - S0y[i]
#         jy_buff[i] = 0

#     one_third = 1.0 / 3.0
#     charge_density = q * w / (dx*dy)
#     factor = charge_density / dt


#     # i and j are the relative shift, 0-based index
#     # [0,   1, 2, 3, 4]
#     #     [-1, 0, 1, 2] for dcell = 1;
#     #     [-1, 0, 1] for dcell_ = 0
#     # [-2, -1, 0, 1] for dcell = -1
#     for j in range(min(1, 1+dcell_y), max(4, 4+dcell_y)):
#         jx_buff = 0.0
#         iy = iy0 + (j - 2)
#         for i in range(min(1, 1+dcell_x), max(4, 4+dcell_x)):
#             ix = ix0 + (i - 2)

#             wx = DSx[i] * (S0y[j] + 0.5 * DSy[j])
#             wy = DSy[j] * (S0x[i] + 0.5 * DSx[i])
#             wz = S0x[i] * S0y[j] + 0.5 * DSx[i] * S0y[j] \
#                 + 0.5 * S0x[i] * DSy[j] + one_third * DSx[i] * DSy[j]

#             jx_buff -= factor * dx * wx
#             jy_buff[i] -= factor * dy * wy

#             jx[ix, iy] += jx_buff
#             jy[ix, iy] += jy_buff[i]
#             jz[ix, iy] += factor * wz * vz
#             rho[ix, iy] += charge_density * S1x[i] * S1y[j]


# @njit(cache=True, parallel=True)
# def unified(
#     e_list, b_list, rho_list, j_list,
#     x0_list, y0_list,
#     pos_list, mom_list, inv_gamma_list,
#     e_part_list, b_part_list,
#     pruned_list,
#     npatches,
#     dx, dy, dt, w_list, q, m,
# ) -> None:
#     for ipatch in prange(npatches):
#         efield = e_list[ipatch]
#         ex = efield[0]
#         ey = efield[1]
#         ez = efield[2]

#         bfield = b_list[ipatch]
#         bx = bfield[0]
#         by = bfield[1]
#         bz = bfield[2]

#         rho = rho_list[ipatch]

#         j = j_list[ipatch]
#         jx = j[0]
#         jy = j[1]
#         jz = j[2]

#         x0 = x0_list[ipatch]
#         y0 = y0_list[ipatch]

#         pos = pos_list[ipatch]
#         x = pos[0]
#         y = pos[1]

#         mom = mom_list[ipatch]
#         ux = mom[0]
#         uy = mom[1]
#         uz = mom[2]

#         e_part = e_part_list[ipatch]
#         ex_part = e_part[0]
#         ey_part = e_part[1]
#         ez_part = e_part[2]
#         b_part = b_part_list[ipatch]
#         bx_part = b_part[0]
#         by_part = b_part[1]
#         bz_part = b_part[2]

#         w = w_list[ipatch][0]
#         inv_gamma = inv_gamma_list[ipatch][0]

#         pruned = pruned_list[ipatch]
#         npart = len(pruned)


#         for ip in range(npart):
#             if pruned[ip]:
#                 continue

#             for idim in range(pos.shape[0]):
#                 pos[idim, ip] += (0.5*c*dt * inv_gamma[ip] * mom[idim, ip])

#             ex_part[ip], ey_part[ip], ez_part[ip], bx_part[ip], by_part[ip], bz_part[ip] = interp(
#                 x[ip], y[ip], dx, dy, x0, y0, ex, ey, ez, bx, by, bz
#             )

#             ux[ip], uy[ip], uz[ip], inv_gamma[ip] = boris_cpu(
#                 ux[ip], uy[ip], uz[ip], 
#                 ex_part[ip], ey_part[ip], ez_part[ip], 
#                 bx_part[ip], by_part[ip], bz_part[ip], 
#                 q, m, dt
#             )
#             for idim in range(pos.shape[0]):
#                 pos[idim, ip] += (0.5*c*dt * inv_gamma[ip] * mom[idim, ip])


#             project(x[ip] - x0, y[ip] - y0, ux[ip], uy[ip], uz[ip], inv_gamma[ip], w[ip], dx, dy, dt, q, jx, jy, jz, rho)