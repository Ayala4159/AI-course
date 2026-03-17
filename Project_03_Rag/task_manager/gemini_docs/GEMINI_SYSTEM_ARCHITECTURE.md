# System Architecture & Logic Flow - Version 1.2

## 1. Data Management Logic
The system is built on a "Flat-File" management style simulated via the `TaskManager` class.
* **State Persistence:** Tasks are stored in memory and synchronized via a Python dictionary-to-JSON serialization process.
* **ID Generation:** Each task is assigned a unique integer ID upon creation to ensure that deletion and status updates don't conflict, even if two tasks have the same title.

## 2. The Polling Mechanism vs. WebSockets
For the MVP, we chose a **Polling approach** (`setInterval(load, 3000)`) over WebSockets.
* **Reasoning:** Since the server is a `SimpleHTTPRequestHandler` (standard library), it doesn't natively support persistent socket connections without third-party libraries like `Flask-SocketIO`. 
* **Efficiency:** Given the low-frequency nature of personal task updates, 3-second polling provides an "almost-real-time" feel without the overhead of maintaining a complex socket state.

## 3. Route Handling Logic
The server implements a custom "Address-Based Router":
1.  **GET /tasks:** Serializes the internal list of Task objects into a JSON array.
2.  **GET /update_status/<id>/<status>:** A semantic URL pattern. The server parses the string, converts the status to the `TaskStatus` Enum, and updates the task object.
3.  **POST /add_task:** Handles `application/x-www-form-urlencoded` data from the HTML form. It includes a fallback for empty descriptions to prevent UI breakage.