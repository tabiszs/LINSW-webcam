"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
#
# # To use a consistent encoding
# from distutils.command.upload import upload as orig
# from distutils.errors import DistutilsError
#
# Always prefer setuptools over distutils
from setuptools import setup
#
# org_upload_file = orig.upload_file
#
#
# def upload_file_ignore_conflict(self, command, pyversion, filename):
#     """ If the PyPi repo already contains a version with the identical name
#     then ignore the conflict exception by not uploading the new file.
#     """
#     print('uploading file with ignore conflict override')
#     try:
#         org_upload_file(self, command, pyversion, filename)
#     except DistutilsError as ex:
#         if 'conflict' in str(ex).lower():
#             print('ignoring conflict, original file stays intact.')
#         else:
#             raise
#
# orig.upload_file = upload_file_ignore_conflict


setup()

