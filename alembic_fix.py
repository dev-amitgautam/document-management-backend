# Run this script to fix alembic configuration
import os

# Path to the alembic/env.py file
env_py_path = 'alembic/env.py'

# Read the current content of the file
with open(env_py_path, 'r') as file:
    content = file.read()

# Add the import for settings and update the connection configuration
updated_content = content.replace(
    "# Import your models and Base",
    """# Import your models and Base
from app.core.config import settings"""
)

# Update the run_migrations_online function to use the database URI from settings
updated_content = updated_content.replace(
    "def run_migrations_online() -> None:",
    """def run_migrations_online() -> None:
    # Override sqlalchemy.url with the one from settings
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.SQLALCHEMY_DATABASE_URI""" 
)

# Write the updated content back to the file
with open(env_py_path, 'w') as file:
    file.write(updated_content)

print(f"Updated {env_py_path} with correct database connection settings.") 