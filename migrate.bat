@echo off
start python migrate.py db migrate
start python create_roles.py
exit