import sys
import numpy as np
from scipy.linalg import expm
import functools
from ..utils.split import split_svd_qr_2tdvp

def phia_next(phi0,mat1,x1,y1,iright):

  if iright == 1: # from right to left
    xx1 = np.conj(x1)
    yy1 = y1
    rtmp2 = np.tensordot(xx1,phi0,axes=((2),(0)))
    if(len(mat1.shape)==4):
      rtmp3 = np.tensordot(rtmp2,mat1,axes=((1,2),(1,3)))
    else:
      rtmp3 = np.einsum('ijkl,mjk->ilmj',rtmp2,mat1)
    phi = np.tensordot(rtmp3,yy1,axes=((1,3),(2,1)))

  else: # from left to right
    xx1 = np.conj(x1)
    yy1 = y1
    rtmp2 = np.tensordot(xx1,phi0,axes=((0),(0)))
    if(len(mat1.shape)==4):
      rtmp3 = np.tensordot(rtmp2,mat1,axes=((0,2),(1,0)))
    else:
      rtmp3 = np.einsum('ijkl,kim->jlim',rtmp2,mat1)
    phi = np.tensordot(rtmp3,yy1,axes=((1,2),(0,1)))
  return phi

#======================================================
def delta_ssol(phi1,phi2,y1):
  rtmp1 = np.tensordot(phi1,y1,axes=((2),(0)))
  dy = np.tensordot(rtmp1,phi2,axes=((1,2),(1,2)))
  dy *= -1.0
  return dy

#==========================================
def delta_ksol(mat1,phi1,phi2,y1):
  rtmp2 = np.tensordot(phi1,y1,axes=((2),(0)))
  if (len(mat1.shape) ==4):
    rtmp3 = np.tensordot(rtmp2,mat1,axes=((1,2),(0,2)))
  else:
    rtmp3 = np.einsum('ijkl,jkm->ilkm',rtmp2,mat1)
  dy = np.tensordot(rtmp3,phi2,axes=((1,3),(2,1)))

  return dy

##=====================================
#def ddot2_ssol(vec1, vec2):
#
#  xx1 = np.conj(vec1)
#  yy1 = vec2
#
#  ddot2 = np.tensordot(xx1,yy1,axes=((0,1), (0,1)))
#  return ddot2
#
##=====================================
#def dnorm2_ssol(vec1):
#
#  dnorm2 = ddot2_ssol(vec1,vec1)
#
#  return np.sqrt(dnorm2)
#
##=====================================
#def ddot2_ksol(vec1, vec2):
#
#  xx1 = np.conj(vec1)
#  yy1 = vec2
#  ddot2 = np.tensordot(xx1,yy1,axes=((0,1,2), (0,1,2)))
#
#  return ddot2
#
##=====================================
#def dnorm2_ksol(vec1):
#
#  dnorm2 = ddot2_ksol(vec1,vec1)
#
#  return np.sqrt(dnorm2)
def ddot2_sol(vec1, vec2):

  xx1 = np.conj(vec1)
  yy1 = vec2
  ddot2 = np.dot(xx1.reshape(-1),yy1.reshape(-1))

  return ddot2


#def dnorm2_sol(vec1):
#
#  dnorm2 = ddot2_sol(vec1,vec1)
#
#  return np.sqrt(dnorm2)

def delta_ksol_td(m1,m2,phi1,phi2,y1,kdims):
#                               1                             0             0
#          |__|__|__|        0__|__3             1            |__1       1__|
#           \_|__|_/    mpo     |      mps    0__|__2  phi1   |     phi2    | 
#                               2                             2             2
  dim1 = phi1.shape
  dim2 = phi2.shape
  dimy = y1.shape
  rx1,ra1,ry1 = dim1
  rx2,ra2,ry2 = dim2

  r1,r2 = split_svd_qr_2tdvp(y1,kdims,small=1e-7)
  rtmp2 = np.tensordot(phi1,r1,axes=((2),(0)))
  rtmp3 = np.tensordot(rtmp2,m1,axes=((1,2),(0,2)))
  rtmp4 = np.tensordot(r2,phi2,axes=((2),(2)))
  rtmp5 = np.tensordot(m2,rtmp4,axes=((2,3),(1,3)))

  dy = np.tensordot(rtmp3,rtmp5,axes=((1,3),(2,0))).reshape(rx1,-1,rx2)

  return dy

def contract_2mps(x1,y1):
  return np.tensordot(x1,y1,axes=((2),(0))).reshape(x1.shape[0],x1.shape[1]*y1.shape[1],y1.shape[2]), (x1.shape[0],x1.shape[1],y1.shape[1],y1.shape[2])

def exvm(rtmp0,hmat,vm):
  exph = expm(hmat)
  ya = np.tensordot(rtmp0*exph[:,0], vm, axes=((0), (0)))
  return ya

def expmv(mmax, dt, yy, phi1, phi2, mat1=None):
#----------------------
  if (mat1 is None):
    delta_v = functools.partial(delta_ssol,phi1=phi1,phi2=phi2)
#    ddot2_v = ddot2_ssol
#    dnorm2_v = dnorm2_ssol
  else:
    delta_v = functools.partial(delta_ksol,mat1=mat1,phi1=phi1,phi2=phi2)
#    ddot2_v = ddot2_ksol
#    dnorm2_v = dnorm2_ksol
  vm = []
  hmat = np.zeros((mmax,mmax),dtype=np.complex128)

#--------------------------
# the first vector
  rtmp0 = np.sqrt(ddot2_sol(yy,yy))
  y0 = yy/rtmp0
  vm.append(y0)
#--------------------------------------------
  for j in range(mmax):
    # dy1
    dy1 = delta_v(y1=vm[j])
#    dy1 *= dt

    # calculate the overlap
    for i in range(j+1):
      hmat[i,j] = ddot2_sol(vm[i], dy1)

    # orthogonaization 
#    for i in range(j+1):
#      dy1 -=  hmat[i,j]*vm[i]
    dy1 -=  np.tensordot(hmat[:j+1,j],vm[:j+1],axes=((0), (0)))

    # new basis
    rtmp = np.sqrt(ddot2_sol(dy1,dy1))
# important, if rtmp = 0, the break, and set array dimension to j
    if (rtmp > 1.e-13):
      if (j < mmax-1):
        hmat[j+1,j] = rtmp
    # need to get a new y0, otherwise not good....
        y0 = dy1/rtmp
        vm.append(y0)
      else:
        print("Warning: The dimension of Krylov space reached mmax")
    else:
      break

  yy = exvm(rtmp0,dt*hmat[:j+1,:j+1],vm[:j+1])
#  jmax = j + 1
##--------------------------------------------
## calculate exp(hmat)
#  exph = expm(hmat[0:jmax,0:jmax])
##--------------------------------------------
## the new yy
#  vtmp = np.zeros(yy.shape,dtype=np.complex128)
#
#  for i in range(jmax):
#    vtmp += rtmp0*exph[i,0]*vm[i]
#
#  yy = vtmp

  return yy

def update_k_2sites(mmax,r1,r2,delta_t,m1,m2,phi1,phi2):
#----------------------
  vm = np.empty((mmax,r1.shape[0],r1.shape[1]*r2.shape[1],r2.shape[2]),dtype=np.complex128)
  hmat = np.zeros((mmax,mmax),dtype=np.complex128)
# the first vector
  yy, kdims = contract_2mps(r1,r2)
  rtmp0 = np.sqrt(ddot2_sol(yy,yy))
#  print(rtmp0)
  dy1 = vm[0] = 1.0/rtmp0*yy
  yy0 = None
#--------------------------------------------
  for j in range(mmax):
    dy1 = delta_ksol_td(m1,m2,phi1,phi2,dy1,kdims)
    # calculate the overlap
    hmat[:j+1,j] = np.dot(np.conj(vm[:j+1]).reshape(j+1,-1), dy1.reshape(-1))
    # orthogonaization 
    dy1 -=  np.tensordot(hmat[:j+1,j],vm[:j+1],axes=((0), (0)))
    # new basis
    rtmp = np.sqrt(ddot2_sol(dy1,dy1))
# important, if rtmp = 0, the break, and set array dimension to j
    if (rtmp < 1.e-13):
      yy = exvm(rtmp0,delta_t*hmat[:j+1,:j+1],vm[:j+1])
      return yy, kdims
    if j > 3:
      yy = exvm(rtmp0,delta_t*hmat[:j+1,:j+1],vm[:j+1])
#      if yy0 is not None and np.sqrt(ddot2_sol(yy-yy0,yy-yy0)) < pa.kryl_thrd:
#      #if yy0 is not None and np.allclose(yy, yy0):
#        return yy, kdims
#      else:
#        yy0 = yy
      yy0 = yy
    if (j < mmax-1):
      hmat[j+1,j] = rtmp
    # need to get a new y0, otherwise not good....
      dy1 /= rtmp
      vm[j+1] = dy1
    else:
      print('Warning: threshold not enough')
  return yy, kdims

def update_rk4(dt,yy,phi1,phi2,mat1=None,rk4slices=10):
  dt1 = dt/rk4slices
  dt2 = dt1/2.0
  dt6 = dt1/6.0
  if (mat1 is None):
    delta_v = functools.partial(delta_ssol,phi1=phi1,phi2=phi2)
  else:
    delta_v = functools.partial(delta_ksol,mat1=mat1,phi1=phi1,phi2=phi2)
  for i in range(rk4slices):
    dy1 = delta_v(y1=yy)
    y0 = yy + dt2*dy1
  
    dy2 = delta_v(y1=y0)
    y0 = yy + dt2*dy2
  
    dy3 = delta_v(y1=y0)
    y0 = yy + dt1*dy3
  
    dy3 = dy2 + dy3
  
    dy2 = delta_v(y1=y0)
  
    yy = yy + dt6*(dy1 + 2.0*dy3 + dy2)

  return yy
