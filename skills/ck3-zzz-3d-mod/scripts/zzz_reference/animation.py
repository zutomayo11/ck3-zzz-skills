"""Explicit T/Q/S input and PDX list-valued trees, without binary backend imports."""
from __future__ import annotations

import re
from typing import Sequence
import xml.etree.ElementTree as ET

import numpy as np

from .validation import finite_array


def continuous_quaternions(rotations) -> np.ndarray:
    q = finite_array(rotations, tail=(4,), label="Quaternions")
    if q.ndim != 3 or min(q.shape[:2]) < 1:
        raise ValueError("Quaternions must be nonempty frames x bones x 4 in xyzw order")
    lengths = np.linalg.norm(q, axis=-1, keepdims=True)
    if np.any(lengths < 1e-12):
        raise ValueError("Zero-length quaternion")
    q = q / lengths
    for frame in range(1, len(q)):
        q[frame, np.sum(q[frame] * q[frame - 1], axis=-1) < 0] *= -1
    return q


def local_matrices(translations, rotations, scales) -> np.ndarray:
    q = continuous_quaternions(rotations)
    t = finite_array(translations, tail=(3,), label="Translations")
    s = finite_array(scales, tail=(3,), label="Scales")
    if t.shape != q.shape[:2] + (3,) or s.shape != t.shape:
        raise ValueError("T/Q/S must share exactly the same frame/bone timeline")
    x, y, z, w = np.moveaxis(q, -1, 0)
    rotation = np.stack((1 - 2*(y*y + z*z), 2*(x*y - z*w), 2*(x*z + y*w),
                         2*(x*y + z*w), 1 - 2*(x*x + z*z), 2*(y*z - x*w),
                         2*(x*z - y*w), 2*(y*z + x*w), 1 - 2*(x*x + y*y)), axis=-1)
    result = np.tile(np.eye(4), q.shape[:2] + (1, 1))
    result[..., :3, :3] = rotation.reshape(q.shape[:2] + (3, 3)) * s[..., None, :]
    result[..., :3, 3] = t
    return result


def _names(names: Sequence[str]) -> list[str]:
    result = list(names)
    if not result or len(set(result)) != len(result) or any(not isinstance(n, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", n) for n in result):
        raise ValueError("Bone aliases must be unique ASCII identifiers")
    return result


def build_anim_tree(names: Sequence[str], translations, rotations, scales, fps: float) -> ET.Element:
    names = _names(names)
    if not np.isfinite(fps) or fps <= 0:
        raise ValueError("FPS must be finite and positive")
    q = continuous_quaternions(rotations)
    t = finite_array(translations, tail=(3,), label="Translations")
    s = finite_array(scales, tail=(3,), label="Scales")
    local_matrices(t, q, s)
    if q.shape[1] != len(names):
        raise ValueError("Bone aliases must match channel order")
    arrays = {"t": t, "q": q, "s": s}
    dynamic = {key: [i for i in range(len(names)) if not np.allclose(value[:, i], value[0, i], rtol=0, atol=1e-8)]
               for key, value in arrays.items()}
    tree = ET.Element("File", {"pdxasset": [1, 0]})
    info = ET.SubElement(tree, "info", {"fps": [float(fps)], "sa": [len(q)], "j": [len(names)]})
    for index, name in enumerate(names):
        flags = "".join(key for key in "tqs" if index in dynamic[key])
        ET.SubElement(info, name, {"sa": [flags], **{key: value[0, index].tolist() for key, value in arrays.items()}})
    ET.SubElement(tree, "samples", {key: value[:, dynamic[key]].ravel().tolist()
                                   for key, value in arrays.items() if dynamic[key]})
    return tree


def decode_anim_tree(tree: ET.Element) -> tuple[np.ndarray, float]:
    info, samples = tree.find("info"), tree.find("samples")
    if info is None or samples is None:
        raise ValueError("Animation needs info and samples")
    nodes = list(info)
    _names([node.tag for node in nodes])
    count, fps = info.get("sa")[0], info.get("fps")[0]
    if not isinstance(count, int) or count < 1 or info.get("j") != [len(nodes)] or not np.isfinite(fps) or fps <= 0:
        raise ValueError("Invalid animation frame/bone count or FPS")
    for node in nodes:
        flags = node.get("sa")[0]
        if not isinstance(flags, str) or any(key not in "tqs" for key in flags) or len(flags) != len(set(flags)):
            raise ValueError("Unknown or duplicate animation channel flags")
    arrays = {}
    for key, width in (("t", 3), ("q", 4), ("s", 3)):
        first = np.array([node.get(key) for node in nodes], dtype=np.float64)
        if key == "s" and first.shape == (len(nodes), 1):
            first = np.repeat(first, 3, axis=1)
        if first.shape != (len(nodes), width) or not np.isfinite(first).all():
            raise ValueError("Invalid first-frame channel values")
        dynamic = [i for i, node in enumerate(nodes) if key in node.get("sa")[0]]
        raw = np.asarray(samples.get(key, []), dtype=np.float64)
        # This reference emits vec3 scales, not mixed scalar/vec3 scale records.
        if raw.size != count * len(dynamic) * width or not np.isfinite(raw).all():
            raise ValueError(f"Truncated or invalid {key} samples")
        arrays[key] = np.repeat(first[None], count, axis=0)
        if dynamic:
            arrays[key][:, dynamic] = raw.reshape(count, len(dynamic), width)
    return local_matrices(arrays["t"], arrays["q"], arrays["s"]), float(fps)
