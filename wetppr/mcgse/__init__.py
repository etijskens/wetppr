# -*- coding: utf-8 -*-

"""
# Module wetppr.mcgse

Case study [Monte Carlo Ground state energy calculation of a small atomistic system][Monte-carlo-ground-state-energy-calculation-of-a-small-atomistic-system].



"""
import typing
from math import pi, sin, cos

import numpy as np

def morse_potential(r: float, D_e: float = 1, alpha: float = 1, r_e: float = 1
					) -> float:
	"""Compute the Morse potential for interatomic distance r.

	This is better than it looks, we can pass a numpy array for r, and it will
	use numpy array arithmetic to evaluate the expression for the array.
	"""
	return D_e * (1 - np.exp(-alpha*(r - r_e)))**2

def interatomic_distance(x: np.ndarray, y: np.ndarray, z: np.ndarray, i: int, j: int) -> float:
	"""Compute the interatomic distance between atoms i and j."""
	return np.sqrt((x[j] - x[i]) ** 2 + (y[j] - y[i]) ** 2 + (z[j] - z[i]) ** 2)

def interatomic_distances(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
	"""Compute the array of interatomic distances."""
	n_atoms = x.shape[0]
	n_pairs = n_atoms * (n_atoms - 1) // 2  # // = integer division
	# Compute the interatomic distances
	rij = np.empty(n_pairs, dtype=float)
	ij = 0
	for i in range(1, n_atoms):
		# we compute an entire row of the lower triangular rij matrix at once
		xj = x[0:i]
		yj = y[0:i]
		zj = z[0:i]
		nj = i  # the number of pairs for we compute the interatomic distance at once
		rij[ij:ij + i] = np.sqrt((xj - x[i]) ** 2 + (yj - y[i]) ** 2 + (zj - z[i]) ** 2)
		ij += i

	return rij


def initialize_random(n_atoms: int) -> typing.Tuple[np.ndarray,np.ndarray,np.ndarray]:
	"""

	Our morse potential has equilibrium distance of 1. An FCC cube with an edge of 1 has 4 atoms. So the number of atoms
	per volume unit is 4. So n atoms should occupy a volume of n/4 or. That is a cube of (n/4)**(1/3).
	"""
	a = (n_atoms/4) ** (1/3)
	x = a * np.random.rand(n_atoms)
	y = a * np.random.rand(n_atoms)
	z = a * np.random.rand(n_atoms)

	return x, y, z


def sample_unit_sphere(n: int =1, *, ndim:int = 3):
	"""Generate n random points on the unit sphere in ndim dimensional space."""

	# Reference: https://mathworld.wolfram.com/SpherePointPicking.html, laast approach, and
	# https://stackoverflow.com/questions/33976911/generate-a-random-sample-of-points-distributed-on-the-surface-of-a-unit-sphere)

	v = np.random.randn(ndim, n)
	v /= np.linalg.norm(v, axis=0)
	return v

def perturb( x: np.ndarray, y: np.ndarray, z: np.ndarray, *, i: int = -1, dist=None):
	"""Perturb the configuration.
	If i==-1, one randomly selected atom is perturbed.
	if 0<=i<n_atoms, the i-tha atom is perturbed.
	If n_atoms<=i, all atoms are perturbed.

    Args:
        x: array of x-coordinates
        y: array of y-coordinates
        z: array of z-coordinates
        i: index of the atom to be displaced. If equal to -1, a random atom is selected.
        dist: a callable dist(n) generates a array of n values. these are use to scale the displacement(s)
        	of the perturbed atom(s).

    Returns:
    	the index of the perturbed atom.
	"""
	n_atoms = len(x)
	if n_atoms<=i:
		# Perturb all atoms:
		v = sample_unit_sphere(n_atoms)
		# scale the displacement
		d = dist(n_atoms)
		v *= d
		# add the displacements to the points
		x += v[0]
		y += v[1]
		z += v[2]
		return n_atoms
	else:
		# select the point do perturb
		i_ = np.random.randint(0,len(x)) if (i == -1) else i
		# generate 1 random 3D displacement direction
		v = sample_unit_sphere()
		# scale the displacement
		d = dist(1)
		v *= d
		# add the displacement to the point
		x[i_] += v[0]
		y[i_] += v[1]
		z[i_] += v[2]
		# debug info
		# print(f"Perturb i = {i_} delta = {np.linalg.norm(v)}")

		return i_

def energy_loop(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> typing.Tuple[float, np.ndarray, np.ndarray]:
	"""Compute the interaction energy for the system with atom coordinates x, y, and z with
	the Morse potential. All poirs are evaluated.

	We use the split loop
	"""
	rij = interatomic_distances(x, y, z)

	# compute the interaction energies
	Eij = morse_potential(rij)
	E = np.sum(Eij)
	return E, Eij, rij


def energy_update( x: np.ndarray, y: np.ndarray, z: np.ndarray, i: int
		  		 , rij: np.ndarray, Eij: np.ndarray, E: float
		  ) -> float:
	"""update the interatomic distances, the interaction energies and the total potential energy.

	Args:
		x: array of x-coordinates (input)
		y: array of y-coordinates (input)
		z: array of z-coordinates (input)
		i: index of the perturbed atom (input)
		rij: array of interatomic distances (input/output)
		Eij: array of pair interaction energies (input/output)
		E: total interaction energy (input/output)
	"""
	# Update rij and Eij
	# update the orange row
	ij = i*(i-1)//2
	xj = x[0:i]
	yj = y[0:i]
	zj = z[0:i]
	rij[ij:ij + i] = np.sqrt((xj - x[i]) ** 2 + (yj - y[i]) ** 2 + (zj - z[i]) ** 2)
	E -= np.sum(Eij[ij:ij + i]) 						# subtract the old values
	Eij[ij:ij + i] = morse_potential(rij[ij:ij + i]) 	# update
	E += np.sum(Eij[ij:ij + i]) 						# add the new values

	# update the orange column
	for j in range(i+1, x.shape[0]):
		ij = j*(j-1)//2 + i
		E -= Eij[ij]  									# subtract the old values
		rij[ij] = interatomic_distance(x,y,z,i,j)		# update rij[ij]
		Eij[ij] = morse_potential(rij[ij]) 				# update Eij[ij]
		E += Eij[ij]  									# add the new values

	return E


def execute_perturbation_loop(
		config: tuple,
		n_iterations: int,
		*,
		dist: typing.Callable,
		algo: str = 'ON',
		verbosity: int = 0
	) -> typing.Tuple[float, np.ndarray, np.ndarray, np.ndarray]:
	"""Run a perturbation loop. 
	
	Args:
		config: a tuple (x,y,z) with atom coordinates.
		n_iterations: number of perturbation iterations.
		dist: distribution from which the length of a perturbation displacement is drawn. See also: perturb().
		algo: 'ON' | 'ON2' select algorithm O(N) or O(N**2)
	Returns:
		the lowest energy and the corresponding configuration. 
	"""
	# Unpack configuration tuple. We take a copy, to avoid modifying the input configuration.
	x = np.copy(config[0])
	y = np.copy(config[1])
	z = np.copy(config[2])
	n_atoms = len(x)
	# Compute energy of initial configuration
	if algo == 'ON':
		E, Eij, rij = energy_loop(x, y, z)  # the first time energy_loop is necessary to create Eij and rij
	else:
		E, _  , _   = energy_loop(x, y, z)
	Emin = E

	if verbosity>=1:
		print(f"{algo} iteration 0: {Emin=}")

	for iter in range(n_iterations):

		if algo == 'ON':
			i = perturb(x, y, z, dist=dist)
			E = energy_update(x, y, z, i, rij, Eij, E)
		else:
			perturb(x, y, z, i=n_atoms, dist=dist)
			E, _, _ = energy_loop(x, y, z)

		if E < Emin:
			Emin = E
			xmin = x
			ymin = y
			zmin = z
			imin = iter+1
			if verbosity >= 2:
				print(f"{algo} iteration {iter+1}: {Emin=}")

	if verbosity >= 1:
		print(f"{algo} iteration {iter + 1}: {Emin=}, last improvement: iteration = {imin}")

	return Emin, xmin, ymin, zmin


class LogNormal:
	"""wrapper for numpy.random.lognormal which stores mean and sigma arguments.

	(Couldn't get functools.partial to work the way I wanted...)."""
	def __init__(self, mean, sigma ):
		self.mean = mean
		self.sigma = sigma
	def __call__(self, n=1):
		return np.random.lognormal(mean=self.mean, sigma=self.sigma, size=n)


if __name__ == "__main__":
	# Randomly distribute 4 points (atoms) on a sphere with diameter 1
	# The ground state is a tetahedron with Emin=0 and rij=1 for all i!=j.
	for i in range(5):
		print()
		sample = sample_unit_sphere(4) * 0.5
		config = (sample[0], sample[1], sample[2])
		dist = LogNormal(mean=-5, sigma=.4)
		Emin_ON2, *config_min_ON2 = execute_perturbation_loop(config=config, n_iterations=200_000, dist=dist, algo='ON2', verbosity=1)
		Emin_ON , *config_min_ON  = execute_perturbation_loop(config=config, n_iterations=200_000, dist=dist, algo='ON' , verbosity=1)

	print("-*# finished #*-")
