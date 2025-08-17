#! /usr/bin/env bash

sqlite3 database.db "create table users (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, age INTEGER NOT NULL, gender TEXT NOT NULL, role TEXT NOT NULL, salary INTEGER)"
sqlite3 database.db "CREATE TABLE admins (id INTEGER PRIMARY KEY, user TEXT UNIQUE NOT NULL, password TEXT UNIQUE NOT NULL, permission TEXT NOT NULL)"
