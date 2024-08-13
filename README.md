# ZLI-Modul-109-inventory-app (Lösung)

## Technologies

- Docker
- Python
- Flask
- PostgreSQL
- OpenLDAP
- HTML
- JavaScript
- OpenShift

---

## How To Use

### Configure openLDAP

1. Login phpLDAPadmin

```html
URL: http://localhost:8080/phpldapadmin/index.php
Login DN: cn=admin,dc=test,dc=ch
Password: admin
```

2. Create a child entry / Simple Security Object

```html
User Name: admin
Password: admin (clear)
```

### Inventory-App Login

```html
URL: http://localhost/
Username: <LDAP Username>
Password: <LDAP Password>
```

### Inventory-App Functions

```html
URL: http://localhost/api_docs.html
```

### Environment Variables

| Variable Name             | Description                                                                                   | Default Value               | Required |
|---------------------------|-----------------------------------------------------------------------------------------------|-----------------------------|----------|
| `POSTGRES_HOST`           | Hostname or IP address of the PostgreSQL database server                                      | `db`                        | Yes      |
| `POSTGRES_USER`           | Username for the PostgreSQL database                                                          | `user`                      | Yes      |
| `POSTGRES_PASSWORD`       | Password for the PostgreSQL database                                                          | `password`                  | Yes      |
| `POSTGRES_DATABASE`       | Name of the PostgreSQL database                                                               | `inventorydb`               | Yes      |
| `PGADMIN_DEFAULT_EMAIL`   | Default email address for the PgAdmin administrator                                           | `admin@example.com`         | Yes      |
| `PGADMIN_DEFAULT_PASSWORD`| Default password for the PgAdmin administrator                                                | `admin`                     | Yes      |
| `BITNAMI_DEBUG`           | Enables debug mode for Bitnami applications (true/false)                                      | `true`                      | No       |
| `LDAP_ADMIN_USERNAME`     | Administrator username for the LDAP server                                                    | `admin`                     | Yes      |
| `LDAP_ADMIN_PASSWORD`     | Administrator password for the LDAP server                                                    | `admin`                     | Yes      |
| `LDAP_USERS`              | List of users for the LDAP server                                                             | `admin`                     | Yes      |
| `LDAP_PASSWORDS`          | List of passwords for the LDAP users                                                          | `admin`                     | Yes      |
| `LDAP_ROOT`               | Root DN (Distinguished Name) for the LDAP directory tree                                      | `dc=test,dc=ch`             | Yes      |
| `LDAP_ADMIN_DN`           | Distinguished Name (DN) of the administrator for the LDAP server                              | `cn=admin,dc=test,dc=ch`    | Yes      |
| `LDAP_PORT_NUMBER`        | Port number for the LDAP server                                                               | `1389`                      | Yes      |
| `LDAP_NAME`               | Name of the LDAP server                                                                       | `ldap`                      | Yes      |
| `LDAP_HOST`               | Hostname or IP address of the LDAP server                                                     | `ldap`                      | Yes      |
| `LDAP_BASE`               | Base DN for search queries in the LDAP directory                                              | `dc=test,dc=ch`             | Yes      |
| `LDAP_BIND_ID`            | Bind ID or DN used for authentication on the LDAP server                                      | `cn=admin,dc=test,dc=ch`    | Yes      |
| `LDAP_PORT`               | Alternative port for the LDAP server                                                          | `1389`                      | Yes      |
| `BACKEND_PROTOCOL`        | Protocol used for communication with the backend (e.g., http or https)                        | `http`                      | Yes      |
| `BACKEND_HOST`            | Hostname or IP address of the backend server                                                  | `localhost`                 | Yes      |
| `BACKEND_PORT`            | Port number for connecting to the backend                                                     | `5001`                      | Yes      |