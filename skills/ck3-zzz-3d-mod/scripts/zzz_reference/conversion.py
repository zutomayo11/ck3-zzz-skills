"""Topology and coordinate references; no Blender scene or source files are loaded."""
from __future__ import annotations

from typing import Mapping

import numpy as np

from .validation import finite_array


def source_faces(raw: Mapping, converted: Mapping) -> list[list[int]]:
    """Verify the sequential source-index layout used by native_mesh_data.py."""
    vertex_count = raw["m_VertexCount"]
    if isinstance(vertex_count, (bool, np.bool_)) or not isinstance(vertex_count, (int, np.integer)) or vertex_count <= 0:
        raise ValueError("Vertex count must be a positive integer")
    if len(raw["m_SubMeshes"]) != len(converted["SubmeshList"]):
        raise ValueError("Native/converter submesh count mismatch")
    faces = []
    cursor = 0
    for native, exported in zip(raw["m_SubMeshes"], converted["SubmeshList"]):
        count = native["indexCount"]
        offset = native["firstVertex"]
        if isinstance(offset, (bool, np.bool_)) or not isinstance(offset, (int, np.integer)) or not 0 <= offset < vertex_count:
            raise ValueError("Submesh firstVertex must be an integer inside the vertex range")
        if native["topology"] != "Triangles" or isinstance(count, (bool, np.bool_)) or not isinstance(count, (int, np.integer)) or count <= 0 or count % 3:
            raise ValueError("Only nonempty original triangle topology is supported")
        original = raw["m_Indices"][cursor:cursor + count]
        cursor += count
        if len(original) != count:
            raise ValueError("Truncated source index buffer")
        triangles = [original[i:i + 3][::-1] for i in range(0, count, 3)]
        reconstructed = []
        for face in exported["FaceList"]:
            indices = face["VertexIndices"]
            if len(indices) != 3 or any(isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, np.integer)) or not 0 <= v < vertex_count - offset for v in indices):
                raise ValueError("Converter local indices must be nonnegative integers inside the submesh vertex range")
            reconstructed.append([v + offset for v in indices])
        if triangles != reconstructed:
            raise ValueError("Converter topology differs from exact native index buffer")
        if any(isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, np.integer)) or not 0 <= v < vertex_count
               for triangle in triangles for v in triangle):
            raise ValueError("Native triangle references an invalid vertex")
        faces.extend(triangles)
    if cursor != len(raw["m_Indices"]) or not faces:
        raise ValueError("Unconsumed or empty native mesh indices")
    return faces


def _basis(value) -> np.ndarray:
    basis = finite_array(value, tail=(4, 4), label="Basis")
    if basis.ndim != 2 or not np.allclose(basis[3], [0, 0, 0, 1], rtol=0, atol=1e-12):
        raise ValueError("Basis must be affine")
    if abs(np.linalg.det(basis[:3, :3])) < 1e-15:
        raise ValueError("Basis must be invertible")
    return basis


def change_basis(matrices, basis) -> np.ndarray:
    """Apply C M C^-1 to local, world, or inverse-bind matrices consistently."""
    matrices = finite_array(matrices, tail=(4, 4), label="Matrices")
    basis = _basis(basis)
    return basis @ matrices @ np.linalg.inv(basis)


def convert_geometry(positions, normals, faces, basis) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    positions = finite_array(positions, tail=(3,), label="Positions")
    normals = finite_array(normals, tail=(3,), label="Normals")
    faces = np.asarray(faces)
    if positions.ndim != 2 or not len(positions) or normals.shape != positions.shape:
        raise ValueError("Positions and normals must be matching nonempty Nx3 arrays")
    if faces.ndim != 2 or faces.shape[1] != 3 or not len(faces) or faces.dtype.kind not in "iu":
        raise ValueError("Faces must be integer triangle indices")
    if np.any(faces < 0) or np.any(faces >= len(positions)):
        raise ValueError("Triangle index outside vertex range")
    basis = _basis(basis)
    converted = positions @ basis[:3, :3].T + basis[:3, 3]
    normal_values = normals @ np.linalg.inv(basis[:3, :3])
    lengths = np.linalg.norm(normal_values, axis=1, keepdims=True)
    if np.any(lengths == 0):
        raise ValueError("Zero-length normal")
    winding = faces[:, ::-1].copy() if np.linalg.det(basis[:3, :3]) < 0 else faces.copy()
    return converted, normal_values / lengths, winding
