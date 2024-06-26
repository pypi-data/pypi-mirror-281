# Copyright © 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from polaris.utils.database.standard_database import DatabaseType, StandardDatabase


def migrate(conn):
    StandardDatabase.for_type(DatabaseType.Demand).add_table(conn, "path_units", None, add_defaults=True)
