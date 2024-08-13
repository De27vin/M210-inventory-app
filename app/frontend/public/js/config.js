/**
 * config.js
 *
 * This module provides various utility functions for handling user authentication,
 * fetching and filtering inventory data, and exporting table data to Excel.
 *
 * Functions:
 * - handleEnterKey: Triggers a login action when the Enter key is pressed.
 * - login: Handles user login, stores the access token and displays the inventory dashboard.
 * - logoff: Logs the user out by removing the access token and hiding the inventory dashboard.
 * - checkLoginStatus: Checks if the user is logged in and whether the token is still valid.
 * - fetchInventoryData: Fetches the inventory data from the backend and populates the table.
 * - filterTable: Filters the inventory table based on user input.
 * - exportToExcel: Exports the current table data to an Excel file.
 *
 * Dependencies:
 * - xlsx.full.min.js: Used for exporting table data to Excel.
 */

// Function that triggers an action when the Enter key is pressed
export function handleEnterKey(event) {
    if (event.key === 'Enter') {
        console.log('Enter key pressed');
        login();
    }
}

// Function to handle user login
export function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const url = `${window.BACKEND_PROTOCOL}://${window.BACKEND_HOST}:${window.BACKEND_PORT}/login`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            console.log('Login successful, token received:', data.access_token);
            const expirationTime = Date.now() + 10 * 60 * 1000; // 10 minutes in milliseconds
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('token_expiration', expirationTime.toString());

            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('inventoryDashboard').style.display = 'block';
            fetchInventoryData();
        } else {
            console.error('Login failed: No access_token received');
            document.getElementById('loginError').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error during login:', error);
        document.getElementById('loginError').style.display = 'block';
    });
}

// Function to handle user logoff
export function logoff() {
    console.log('Logoff function called');
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_expiration');
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('inventoryDashboard').style.display = 'none';
}

// Function that checks if the user is logged in and if the token is still valid
export function checkLoginStatus() {
    const token = localStorage.getItem('access_token');
    const expiration = localStorage.getItem('token_expiration');

    console.log('Checking token:', token);
    console.log('Token expiration time:', expiration);

    if (token && expiration) {
        const expirationTime = parseInt(expiration, 10);
        if (Date.now() < expirationTime) {
            console.log('Token is valid');
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('inventoryDashboard').style.display = 'block';
            fetchInventoryData();
        } else {
            console.log('Token has expired');
            logoff();
        }
    } else {
        console.log('No token or token has expired');
        logoff();
    }
}

// Function to fetch inventory data from the backend
export function fetchInventoryData() {
    console.log('Fetching inventory data');
    const url = `${window.BACKEND_PROTOCOL}://${window.BACKEND_HOST}:${window.BACKEND_PORT}/inventory`;
    const token = localStorage.getItem('access_token');

    fetch(url, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Inventory data received', data);
        const inventoryBody = document.getElementById('inventoryBody');
        inventoryBody.innerHTML = ''; 
        data.forEach(item => {
            const row = `<tr>
                <td>${item.id}</td>
                <td><a href="details.html?id=${item.id}">${item.servername}</a></td>
                <td>${item.os}</td>
                <td>${item.environment}</td>
                <td>${item.application_id}</td>
            </tr>`;
            inventoryBody.innerHTML += row;
        });
    })
    .catch(error => {
        console.error('Error fetching inventory data:', error);
    });
}

// Function to filter the inventory table based on user input
export function filterTable() {
    console.log('Filtering table');
    const servernameFilter = document.getElementById('servernameFilter').value.toLowerCase();
    const osFilter = document.getElementById('osFilter').value.toLowerCase();
    const appIdFilter = document.getElementById('appIdFilter').value.toLowerCase();
    const envFilter = document.getElementById('envFilter').value.toLowerCase();

    const rows = document.querySelectorAll('#inventoryBody tr');

    rows.forEach(row => {
        const servername = row.cells[1].textContent.toLowerCase();
        const os = row.cells[2].textContent.toLowerCase();
        const appId = row.cells[4].textContent.toLowerCase();
        const environment = row.cells[3].textContent.toLowerCase();

        console.log('Row data:', { servername, os, appId, environment });

        const matchesServername = servername.includes(servernameFilter);
        const matchesOS = os.includes(osFilter);
        const matchesAppId = appId.includes(appIdFilter);
        const matchesEnv = environment.includes(envFilter);

        console.log('Matches:', { matchesServername, matchesOS, matchesAppId, matchesEnv });

        if (matchesServername && matchesOS && matchesAppId && matchesEnv) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Function to export the current table data to an Excel file
export function exportToExcel() {
    console.log('Exporting to Excel');
    
    const table = document.getElementById('inventoryTable');
    const workbook = XLSX.utils.table_to_book(table, {sheet: "Inventory"});
    XLSX.writeFile(workbook, 'inventory.xlsx');
}

// Check login status when the page loads
window.onload = checkLoginStatus;
