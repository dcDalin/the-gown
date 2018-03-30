# the_gown/api/models.py
"""This is the Model

This module does imitates a relational database by usage of lists as tables
"""


class TheGown(object):
    """The main model class, think of it as a database called The Gown"""

    def __init__(self):
        """Constructor method. Contains lists, think of them as tables"""
        self.users = []
