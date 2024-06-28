import shutil
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest

from scikit_build_core.build import build_sdist, build_wheel

DIR = Path(__file__).parent.resolve()
SIMPLEST = DIR / "packages/simplest_c"


def test_pep517_sdist(tmp_path, monkeypatch):
    dist = tmp_path.resolve() / "dist"
    monkeypatch.chdir(SIMPLEST)
    if Path("dist").is_dir():
        shutil.rmtree("dist")

    out = build_sdist(str(dist))

    (sdist,) = dist.iterdir()
    assert sdist.name == "simplest-0.0.1.tar.gz"
    assert sdist == dist / out

    with tarfile.open(sdist) as f:
        file_names = set(f.getnames())
        assert file_names == {
            f"simplest-0.0.1/{x}"
            for x in (
                "CMakeLists.txt",
                "pyproject.toml",
                ".gitignore",
                "src/module.c",
                "src/simplest/__init__.py",
                "src/simplest/_module.pyi",
                "src/simplest/data.txt",
                "src/simplest/sdist_only.txt",
                "src/not_a_package/simple.txt",
                "src/simplest/excluded.txt",
                "PKG-INFO",
            )
        }


@pytest.mark.compile()
@pytest.mark.configure()
@pytest.mark.parametrize(
    "component", [[], ["PythonModule"], ["PythonModule", "Generated"]]
)
def test_pep517_wheel(tmp_path, monkeypatch, virtualenv, component):
    dist = tmp_path / "dist"
    dist.mkdir()
    monkeypatch.chdir(SIMPLEST)
    if Path("dist").is_dir():
        shutil.rmtree("dist")
    out = build_wheel(str(dist), config_settings={"install.components": component})
    (wheel,) = dist.glob("simplest-0.0.1-*.whl")
    assert wheel == dist / out

    virtualenv.install(wheel)

    if sys.version_info >= (3, 8):
        with wheel.open("rb") as f:
            p = zipfile.Path(f)
            file_names = {x.name for x in p.iterdir()}
            simplest_pkg = {x.name for x in p.joinpath("simplest").iterdir()}

        filtered_pkg = {x for x in simplest_pkg if not x.startswith("_module")}
        if not component or "PythonModule" in component:
            assert filtered_pkg != simplest_pkg
        else:
            assert filtered_pkg == simplest_pkg

        expected_wheel_files = {
            "__init__.py",
            "data.txt",
            "excluded.txt",
            "sdist_only.txt",
        }

        if not component:
            expected_wheel_files.add("generated_ignored.txt")
            expected_wheel_files.add("generated_no_wheel.txt")

        if not component or "Generated" in component:
            expected_wheel_files.add("generated.txt")

        assert len(filtered_pkg) == len(simplest_pkg) - 2
        assert {"simplest-0.0.1.dist-info", "simplest"} == file_names
        assert expected_wheel_files == filtered_pkg
        # Note that generated_ignored.txt is here because all CMake installed files are
        # present, CMake has the final say.

    version = virtualenv.execute("from simplest import square; print(square(2))")
    assert version == "4.0"


@pytest.mark.compile()
@pytest.mark.configure()
def test_pep517_wheel_incexl(tmp_path, monkeypatch, virtualenv):
    dist = tmp_path / "dist"
    dist.mkdir()
    monkeypatch.chdir(SIMPLEST)
    if Path("dist").is_dir():
        shutil.rmtree("dist")

    out = build_wheel(
        str(dist),
        {
            "sdist.include": "src/simplest/*included*.txt",
            "sdist.exclude": "src/simplest/*excluded*.txt",
            "wheel.exclude": [
                "simplest/sdist_only.txt",
                "simplest/generated_no_wheel.txt",
            ],
            "wheel.packages": ["src/simplest", "src/not_a_package"],
        },
    )

    (wheel,) = dist.glob("simplest-0.0.1-*.whl")
    assert wheel == dist / out

    virtualenv.install(wheel)

    with wheel.open("rb") as f:
        file_names = set(zipfile.ZipFile(f).namelist())

    simplest_pkg = {
        x.split("/", maxsplit=1)[-1] for x in file_names if x.startswith("simplest/")
    }
    not_a_pkg = {
        x.split("/", maxsplit=1)[-1]
        for x in file_names
        if x.startswith("not_a_package/")
    }
    metadata_items = {
        x.split("/", maxsplit=1)[-1]
        for x in file_names
        if x.startswith("simplest-0.0.1.dist-info/")
    }

    assert {
        "licenses/LICENSE.txt",
        "metadata_file.txt",
        "RECORD",
        "METADATA",
        "WHEEL",
    } == metadata_items

    filtered_pkg = {x for x in simplest_pkg if not x.startswith("_module")}

    assert len(filtered_pkg) == len(simplest_pkg) - 2
    assert {"simplest-0.0.1.dist-info", "simplest", "not_a_package"} == {
        x.split("/")[0] for x in file_names
    }
    assert {
        "__init__.py",
        "data.txt",
        "ignored_included.txt",
        "generated.txt",
        "generated_ignored.txt",
    } == filtered_pkg
    assert {"simple.txt"} == not_a_pkg

    version = virtualenv.execute(
        "from simplest import square; print(square(2))",
    )
    assert version == "4.0"
