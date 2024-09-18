#!/bin/sh
set -e
shift
until mariadb -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" "${DB_NAME}" -e 'select 1'; do
  sleep 3
done
python manage.py migrate --fake-initial
until mariadb -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" "${DB_NAME}" -e 'INSERT INTO auth_user
(password, username, is_active, is_superuser, first_name, last_name, email, is_staff, date_joined)
SELECT users.sha256, users.username, 1, 0, "", "", "", 0, "0000-01-01 00:00:00"
FROM users;'; do
  sleep 1
done
exec "$@"
