# -*- coding: utf-8 -*-

"""
# Module wetppr.mcgse

Case study [Monte Carlo Ground state energy calculation of a small atomistic system][Monte-carlo-ground-state-energy-calculation-of-a-small-atomistic-system].

"""
import typing

import numpy as np

def morse_potential(r: float, D_e: float = 1, alpha: float = 1, r_e: float = 1
					) -> float:
	"""Compute the Morse potential for interatomic distance r.

	This is better than it looks, we can pass a numpy array for r, and it will
	use numpy array arithmetic to evaluate the expression for the array.
	"""
	return D_e * (1 - np.exp(-alpha*(r - r_e)))**2


def interatomic_distances(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
	"""Compute the array of interatomic distances."""
	n_atoms = x.shape[0]
	n_pairs = n_atoms * (n_atoms - 1) // 2  # // = integer division
	# Compute the interatomic distances
	rij = np.empty(n_pairs, dtype=float)
	ij = 0
	for i in range(1, n_atoms):
		# we compute an entire row of the lower trinagular rij matrix at once
		xj = x[0:i]
		yj = y[0:i]
		zj = z[0:i]
		nj = i  # the number of pairs for we compute the interatomic distance at once
		rij[ij:ij + i] = np.sqrt((xj - x[i]) ** 2 + (yj - y[i]) ** 2 + (zj - z[i]) ** 2)
		ij += i

	return rij


def energy_loop_full(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> float:
	"""Compute the interaction energy for the system with atom coordinates x, y, and z with
	the Morse potential. All poirs are evaluated.

	We use the split loop
	"""
	rij = interatomic_distances(x, y, z)

	# compute the interaction energies
	Eij = morse_potential(rij)
	E = np.sum(Eij)
	return E


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


def perturb( x: np.ndarray
		   , y: np.ndarray
		   , z: np.ndarray
		   , i: int
		   , w: float ):
	"""perturb the i-t atom w units in a random direction"""
	rn = np.random.rand(3)
	rn *= w * np.sqrt( np.dot(rn,rn) )
	x[i] += rn[0]
	y[i] += rn[1]
	z[i] += rn[2]

def update( x: np.ndarray
		  , y: np.ndarray
		  , z: np.ndarray
		  , rij: np.ndarray
		  , Eij: np.ndarray
		  , E
		  , i: int
		  ):
	"""update the interatomic distances and the potential .
	"""
	