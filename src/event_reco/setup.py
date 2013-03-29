# mv RegressionData.py RegressionData.pyx
# python setup.py build_ext --inplace
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup (
  name = "RegressionData",
  ext_modules = [
    Extension("CRegressionData", ["RegressionData.pyx"])
  ],
  cmdclass = {"build_ext": build_ext}
)
