"""Unit tests of the cryodrgn_utils gen_mask command."""

import pytest
import os
from hashlib import md5
from cryodrgn.utils import run_command


def hash_file(filename: str) -> str:
    assert os.path.exists(filename)

    with open(filename, "rb") as f:
        file_hash = md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)

    return file_hash.hexdigest()


@pytest.mark.parametrize("volume", ["toy-small", "spike"], indirect=True)
@pytest.mark.parametrize("dist", [2, 5])
@pytest.mark.parametrize("dilate", [3, 7])
@pytest.mark.parametrize("apix", [1, 2.79])
def test_mask_fidelity(tmpdir, volume, dist, dilate, apix) -> None:
    """Test that we can compare two volumes produced during reconstruction training."""
    mask_file = os.path.join(tmpdir, f"{volume.label}_mask.mrc")
    out0, err = run_command(
        f"cryodrgn_utils gen_mask {volume.path} {mask_file} "
        f"--dist {dist} --dilate {dilate} --Apix {apix}"
    )
    assert err == ""

    thresh_vals = {"toy-small": 0.5, "spike": 12.472}
    assert (
        round(float(out0.split("\n")[0].split("Threshold=")[1]), 4)
        == thresh_vals[volume.label]
    )

    mask_hashes = {
        "toy-small": {
            2: {
                3: {
                    1: "85f8073b2a933f7d3fb0f890d8630af8",
                    2.79: "26699762b135761eb5b3c8dfcc7ee690",
                },
                7: {
                    1: "b073bfd7a9ae12a6dbf61fc822845524",
                    2.79: "1f92cc29abbe7708286ac1ac91da477a",
                },
            },
            5: {
                3: {
                    1: "71b5eb59642a8ffd012d47d805c3de5c",
                    2.79: "a3abeb31ee91561f2a4483704dd3f95c",
                },
                7: {
                    1: "1037b5733e3c499d932592ac8574496d",
                    2.79: "219cf27948e9f6fd3a720ec6049797dd",
                },
            },
        },
        "spike": {
            2: {
                3: {
                    1: "669db4697acc9d3888cc49852c66c1bd",
                    2.79: "ab1bfedefb583f43e54bd12eda5e5e42",
                },
                7: {
                    1: "683e870c6c91e9316b35cc62decc82e1",
                    2.79: "eb65cbb230e8c5e7187a38e0f3d5aafe",
                },
            },
            5: {
                3: {
                    1: "6607d96c02c35815b3fd01d04201ed50",
                    2.79: "cb8e7b3fb0e142c4f03cb3437649831c",
                },
                7: {
                    1: "b298278a4d9d61adc5ca9543b4a6a218",
                    2.79: "994db98752ebfa1940c373b26c7196b2",
                },
            },
        },
    }
    assert hash_file(mask_file) == mask_hashes[volume.label][dist][dilate][apix]


@pytest.mark.parametrize("volume", ["toy-small"], indirect=True)
@pytest.mark.parametrize("dist_val", [3, 5])
def test_png_output_file(tmpdir, volume, dist_val) -> None:
    mask_file = os.path.join(tmpdir, f"{volume.label}_{dist_val}_mask.mrc")
    plot_file = os.path.join(tmpdir, f"{volume.label}_{dist_val}_slices.png")

    out0, err = run_command(
        f"cryodrgn_utils gen_mask {volume.path} {mask_file} "
        f"-p {plot_file} --dist {dist_val}"
    )
    assert err == ""

    thresh_vals = {"toy-small": 0.5, "spike": 12.472, "50S-vol": 1.2661}
    assert (
        round(float(out0.split("\n")[0].split("Threshold=")[1]), 4)
        == thresh_vals[volume.label]
    )

    mask_hashes = {
        3: {
            "toy-small": "eafaaafd35bdbbdc880802367f892921",
        },
        5: {
            "toy-small": "3ddb1ca57d656d9b8bbc2cf2b045c3b8",
        },
    }
    assert hash_file(mask_file) == mask_hashes[dist_val][volume.label]

    plot_hashes = {
        3: {
            "toy-small": "88d713543bd093d3cba30a6b27ef0a34",
        },
        5: {
            "toy-small": "f112135a63307a8baadba51c6f97150e",
        },
    }
    assert hash_file(plot_file) == plot_hashes[dist_val][volume.label]
