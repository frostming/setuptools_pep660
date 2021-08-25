"""
Create a wheel that, when installed, will make the source package 'editable'
(add it to the interpreter's path, including metadata) per PEP 660. Replaces
'setup.py develop'. Based on the setuptools develop command.
"""

# TODO doesn't behave when called outside the hook

import os
import sys
import time
import base64

from distutils.core import Command
from distutils.errors import DistutilsError

import pkg_resources

SOURCE_EPOCH_ZIP = 499162860


class editable_wheel(Command):
    """Build 'editable' wheel for development"""

    description = "create a PEP 660 'editable' wheel"

    user_options = [
        ("dist-dir=", "d", "directory to put final built distributions in"),
    ]

    boolean_options = []

    def run(self):
        self.build_editable_wheel()

    def initialize_options(self):
        self.dist_dir = None

    def finalize_options(self):
        # is this part of the 'develop' command needed?
        ei = self.get_finalized_command("egg_info")
        if ei.broken_egg_info:
            template = "Please rename %r to %r before using 'develop'"
            args = ei.egg_info, ei.broken_egg_info
            raise DistutilsError(template % args)
        self.args = [ei.egg_name]

        # the .pth file should point to target
        self.egg_base = ei.egg_base
        self.target = pkg_resources.normalize_path(self.egg_base)
        self.dist_info_dir = os.path.basename(
            ei.egg_info[: -len(".egg-info")] + ".dist-info"
        )

    def build_editable_wheel(self):
        if getattr(self.distribution, "use_2to3", False):
            raise NotImplementedError("2to3 not supported")

        di = self.get_finalized_command("dist_info")
        di.egg_base = self.dist_dir
        di.finalize_options()
        self.run_command("dist_info")

        # Build extensions in-place
        self.reinitialize_command("build_ext", inplace=1)
        self.run_command("build_ext")

        # now build the wheel
        # with the dist-info directory and .pth from 'editables' library
        # ...

        import zipfile

        dist_dir = self.dist_dir
        dist_info_dir = self.dist_info_dir
        dist_info_path = os.path.join(dist_dir, dist_info_dir)
        fullname = self.distribution.metadata.get_fullname()
        # superfluous 'ed' tag is only a hint to the user,
        # and guarantees we can't overwrite the normal wheel
        pytag = "py2.py3" if sys.version_info < (3,) else "py3"
        wheel_name = "{}-ed.{}-none-any.whl".format(fullname, pytag)
        wheel_path = os.path.join(dist_dir, wheel_name)

        wheelmeta_builder(os.path.join(dist_info_path, "WHEEL"))

        if os.path.exists(wheel_path):
            os.unlink(wheel_path)

        wheel_dist_info = "{}.dist-info".format(fullname)
        with zipfile.ZipFile(
            wheel_path, "a", compression=zipfile.ZIP_DEFLATED
        ) as archive:
            pth_file = "{}.pth".format(self.distribution.metadata.name)
            pth_content = "{}\n".format(self.target).encode("utf8")
            # copy .pth file
            archive.writestr(
                zipfile.ZipInfo(pth_file, time.gmtime(SOURCE_EPOCH_ZIP)[:6]),
                pth_content,
            )

            # copy .dist-info directory
            for f in sorted(os.listdir(dist_info_path)):
                with open(os.path.join(dist_info_path, f)) as metadata:
                    archive.writestr(
                        zipfile.ZipInfo(
                            os.path.join(wheel_dist_info, f).replace("\\", "/"),
                            time.gmtime(SOURCE_EPOCH_ZIP)[:6],
                        ),
                        metadata.read(),
                    )

            add_manifest(archive, wheel_dist_info)


def urlsafe_b64encode(data):
    """urlsafe_b64encode without padding"""
    return base64.urlsafe_b64encode(data).rstrip(b"=")


# standalone wheel helpers based on enscons
def add_manifest(archive, dist_info_dir):
    """
    Add the wheel manifest.
    """
    import hashlib
    import zipfile

    lines = []
    for f in archive.namelist():
        data = archive.read(f)
        size = len(data)
        digest = hashlib.sha256(data).digest()
        digest = "sha256=" + (urlsafe_b64encode(digest).decode("ascii"))
        lines.append("%s,%s,%s" % (f.replace(",", ",,"), digest, size))

    record_path = os.path.join(dist_info_dir, "RECORD").replace("\\", "/")
    lines.append(record_path + ",,")
    RECORD = "\n".join(lines)
    archive.writestr(
        zipfile.ZipInfo(record_path, time.gmtime(SOURCE_EPOCH_ZIP)[:6]), RECORD
    )
    archive.close()


def wheelmeta_builder(target):
    with open(target, "w+") as f:
        f.write(
            """Wheel-Version: 1.0
Generator: setuptools_pep660 (0.1)
Root-Is-Purelib: false
Tag: py3-none-any
Tag: ed-none-any
"""
        )
