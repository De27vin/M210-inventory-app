CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    servername VARCHAR(255),
    ip VARCHAR(15),
    netmask VARCHAR(15),
    netzzone VARCHAR(50),
    environment VARCHAR(50),
    os VARCHAR(50),
    kernel_version VARCHAR(50),
    application_id INTEGER,
    av VARCHAR(100),
    bv VARCHAR(100),
    virtualisierung VARCHAR(50),
    hardware VARCHAR(100),
    firmware VARCHAR(50),
    cpu INTEGER,
    memory VARCHAR(50),
    cmdb_status VARCHAR(50),
    uptime VARCHAR(50),
    lastupdate TIMESTAMP
);

INSERT INTO inventory (servername, ip, netmask, netzzone, environment, os, kernel_version, application_id, av, bv, virtualisierung, hardware, firmware, cpu, memory, cmdb_status, uptime, lastupdate) VALUES
('lnx1000.prod.test.ch', '192.168.40.1', '255.255.255.240', 'ZIIp', 'PROD', 'RHEL 9.1', '2.6.32-754.50.1.el9.x86_64', 1001, 'Hans Muster', 'Max Muster', 'n/a', 'ProLiant_BL465c_Gen8', 'A26:03/07/2016', 16, '32189 MB', 'Deployed', '68 days', '2024-07-04 16:21:01');

