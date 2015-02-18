from setuptools import setup
from setuptools.extension import Extension
import numpy as np
import os

NAME = 'pyFaceTracker'
PACKAGE_NAME = 'facetracker'
VERSION = '0.1.1'
DESCRIPTION = 'A python wrapper for the FaceTracker library by Jason Mora Saragih'
LONG_DESCRIPTION = """
pyfacetracker is a thin wrapper around FaceTracker. It enables using
FaceTracker while enjoyging the comfort of the Python scripting language.
FaceTracker is a library for deformable face tracking written in C++ using
OpenCV 2, authored by Jason Saragih and maintained by Kyle McDonald.
"""
AUTHOR = 'Amit Aides'
EMAIL = 'amitibo@tx.technion.ac.il'
URL = 'https://bitbucket.org/amitibo/pyfacetracker'
KEYWORDS = ["Face Tracking", "Image Processing", "Video Processing"]
LICENSE = 'See separate LICENSE file'
CLASSIFIERS = [
    'License :: Other/Proprietary License',
    'Development Status :: 3 - Alpha',
    'Topic :: Scientific/Engineering'
]

OPENCV_BASE = r'/usr/local/Cellar/opencv'
OPENCV_LIB_DIRS=[OPENCV_BASE + r'/2.4.10.1/lib']
OPENCV_VERSION = '.2.4.10'

FACETRACKER_BASE = r'/Users/skas/Documents/Uni/Year-3/Research/Programming/FaceTracker'

OPENCV_INCLUDE_DIRS = [
    OPENCV_BASE + p for p in (
        r'\include',
        r'\modules\core\include',
        r'\modules\imgproc\include',
        r'\modules\video\include',
        r'\modules\features2d\include',
        r'\modules\flann\include',
        r'\modules\calib3d\include',
        r'\modules\objdetect\include',
        r'\modules\legacy\include'
    )
]

OPENCV_LIBS=[
    l % OPENCV_VERSION for l in (
        'opencv_core%s',
        'opencv_imgproc%s',
        'opencv_calib3d%s',
        'opencv_video%s',
        'opencv_features2d%s',
        'opencv_ml%s',
        'opencv_highgui%s',
        'opencv_objdetect%s',
        'opencv_contrib%s',
        'opencv_legacy%s'
    )
]


def main():
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        license=LICENSE,
        packages=[PACKAGE_NAME],
        ext_modules = [
           Extension(
                PACKAGE_NAME + '.' + "_facetracker",
                [os.path.join(FACETRACKER_BASE, f) for f in
                    (
                        "src/lib/PDM.cc",
                        "src/lib/PAW.cc",
                        "src/lib/Patch.cc",
                        "src/lib/IO.cc",
                        "src/lib/FDet.cc",
                        "src/lib/FCheck.cc",
                        "src/lib/CLM.cc",
                        "src/lib/Tracker.cc"
                    )
                ] + ["src/_pyFaceTracker.cpp"],
                include_dirs=[os.path.join(FACETRACKER_BASE, 'include')] + OPENCV_INCLUDE_DIRS + [np.get_include()],
                libraries=OPENCV_LIBS,
                library_dirs=OPENCV_LIB_DIRS
            )
        ]
    )


if __name__ == '__main__':
    main()