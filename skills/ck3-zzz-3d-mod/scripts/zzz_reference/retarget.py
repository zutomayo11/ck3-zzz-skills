"""Rotation-only reference from sunna_actions; no actor or bone-name catalogue."""
from __future__ import annotations

from typing import Mapping

import numpy as np

from .validation import finite_array, validate_parents


def rotation(matrices) -> np.ndarray:
    matrices = finite_array(matrices, tail=(4, 4), label="Transforms")
    upper = matrices[..., :3, :3]
    if np.any(np.abs(np.linalg.det(upper)) < 1e-12):
        raise ValueError("Singular/zero-scale transforms have no recoverable rotation")
    u, _, v = np.linalg.svd(upper)
    result = u @ v
    if np.any(np.linalg.det(result) < 0):
        raise ValueError("Reflected transform cannot be treated as a rotation")
    return result


def worlds(local, parents) -> np.ndarray:
    local = finite_array(local, tail=(4, 4), label="Local transforms")
    if local.ndim != 4 or not len(local):
        raise ValueError("Local transforms must be frames x bones x 4 x 4")
    parents = validate_parents(parents, local.shape[1])
    result = np.empty_like(local)
    for index, parent in enumerate(parents):
        result[:, index] = result[:, parent] @ local[:, index] if parent >= 0 else local[:, index]
    return result


def bind_corrections(target_bind, source_bind, pairs: Mapping[int, int]) -> dict[int, tuple[int, np.ndarray]]:
    target = finite_array(target_bind, tail=(4, 4), label="Target bind")
    source = finite_array(source_bind, tail=(4, 4), label="Source bind")
    if target.ndim != 3 or source.ndim != 3 or not len(target) or not len(source) or not pairs:
        raise ValueError("Bind correction needs two skeletons and explicit target-to-source pairs")
    target_rotation, source_rotation = rotation(target), rotation(source)
    result = {}
    for target_index, source_index in pairs.items():
        if not isinstance(target_index, int) or not isinstance(source_index, int) or not 0 <= target_index < len(target) or not 0 <= source_index < len(source):
            raise ValueError("Bone mapping index outside skeleton")
        result[target_index] = (source_index, source_rotation[source_index].T @ target_rotation[target_index])
    return result


def solve(rest_local, parents, desired: Mapping[int, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    """One frame: replace mapped rotations, retaining native local translations/scales."""
    rest = finite_array(rest_local, tail=(4, 4), label="Native rest")
    if rest.ndim != 3:
        raise ValueError("Rest transforms must be bones x 4 x 4")
    if not np.allclose(rest[:, 3], [0, 0, 0, 1], rtol=0, atol=1e-12):
        raise ValueError("Rest transforms must be affine")
    parents = validate_parents(parents, len(rest))
    for index, value in desired.items():
        if not isinstance(index, int) or not 0 <= index < len(rest):
            raise ValueError("Mapped target index outside skeleton")
        value = finite_array(value, tail=(3, 3), label="Desired rotation")
        if value.ndim != 2 or not np.allclose(value.T @ value, np.eye(3), rtol=0, atol=1e-6) or not np.isclose(np.linalg.det(value), 1, rtol=0, atol=1e-6):
            raise ValueError("Desired transforms must be proper world rotations")
    local = rest.copy()
    world = np.empty_like(local)
    for index, parent in enumerate(parents):
        parent_world = world[parent] if parent >= 0 else np.eye(4)
        if index in desired:
            scale = np.linalg.norm(rest[index, :3, :3], axis=0)
            original_rotation = rotation(rest[index])
            if not np.allclose(original_rotation * scale, rest[index, :3, :3], rtol=0, atol=2e-5):
                raise ValueError("Rest shear cannot be represented by rotation and scale")
            local[index, :3, :3] = rotation(parent_world).T @ np.asarray(desired[index]) @ np.diag(scale)
        world[index] = parent_world @ local[index]
    return local, world
