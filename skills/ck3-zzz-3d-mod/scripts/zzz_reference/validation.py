"""Checks adapted from validate_export.py and sunna_actions/format.py."""
from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Iterable

import numpy as np


def finite_array(value, *, tail: tuple[int, ...], label: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.float64)
    if result.ndim < len(tail) or result.shape[-len(tail):] != tail or not np.isfinite(result).all():
        raise ValueError(f"{label}: expected finite arrays ending in {tail}")
    return result


def validate_parents(parents: Iterable[int], count: int) -> list[int]:
    result = list(parents)
    if count < 1 or len(result) != count:
        raise ValueError("Parent array must match a nonempty skeleton")
    for index, parent in enumerate(result):
        if isinstance(parent, (bool, np.bool_)) or not isinstance(parent, (int, np.integer)) or not -1 <= parent < index:
            raise ValueError("Skeleton must be parent-first; roots use -1")
    return result


def validate_skin(indices, weights, bone_count: int, *, tolerance: float = 1e-4) -> None:
    indices = np.asarray(indices)
    weights = finite_array(weights, tail=(4,), label="Skin weights")
    if weights.ndim != 2 or not len(weights) or indices.shape != weights.shape or indices.dtype.kind not in "iu":
        raise ValueError("Skin requires four integer index/weight slots per vertex")
    if isinstance(bone_count, (bool, np.bool_)) or not isinstance(bone_count, (int, np.integer)) or bone_count < 1:
        raise ValueError("Bone count must be a positive integer")
    if tolerance < 0 or not np.isfinite(tolerance):
        raise ValueError("Invalid bone count or weight tolerance")
    used = (indices >= 0) & (indices < bone_count)
    unused = (indices == -1) & (weights == 0)
    if not np.all(used | unused) or np.any(weights < 0):
        raise ValueError("Unknown bone index, nonzero unused slot, or negative weight")
    if np.any(np.abs(weights.sum(axis=1) - 1) > tolerance):
        raise ValueError("Skin weights must sum to one; repair at the source")


def validate_roundtrip(expected, actual, *, absolute: float = 3e-5, relative: float = 1.3e-7) -> float:
    expected = np.asarray(expected, dtype=np.float64)
    actual = np.asarray(actual, dtype=np.float64)
    if expected.shape != actual.shape or not expected.size or not np.isfinite(expected).all() or not np.isfinite(actual).all():
        raise ValueError("Roundtrip shape/frame count or finite values differ")
    if not np.isfinite([absolute, relative]).all() or min(absolute, relative) < 0:
        raise ValueError("Roundtrip tolerances must be finite and nonnegative")
    error = np.abs(actual - expected)
    if np.any(error > np.maximum(absolute, np.abs(expected) * relative)):
        raise ValueError(f"Roundtrip exceeds tolerance: {float(error.max())}")
    return float(error.max())


def resolve_references(references: Iterable[str], roots: Iterable[Path]) -> dict[str, Path]:
    """Roots are supplied in highest-priority-first order; this is file lookup only."""
    roots = [Path(root).resolve() for root in roots]
    if not roots or any(not root.is_dir() for root in roots):
        raise ValueError("Reference roots must be existing directories")
    result = {}
    for reference in references:
        if not isinstance(reference, str) or not reference or "\0" in reference or ":" in reference:
            raise ValueError("Reference must be a relative file path")
        relative = PurePosixPath(reference.replace("\\", "/"))
        if relative.is_absolute() or ".." in relative.parts or not relative.parts:
            raise ValueError("Reference escapes its root")
        for root in roots:
            candidate = root.joinpath(*relative.parts).resolve()
            if not candidate.is_relative_to(root):
                raise ValueError("Reference follows a link outside its root")
            if candidate.is_file():
                result[reference] = candidate
                break
        else:
            raise FileNotFoundError(reference)
    return result
