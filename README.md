# Split App Postman Collection

This repository contains the Postman collection for the Split App API, used to test and interact with the backend endpoints.

---

## How to Import the Postman Collection

1. Download the `split-app-postman-collection.json` file from this repository.

2. Open [Postman](https://www.postman.com/).

3. In Postman, click **Import** (top-left corner).

4. Select **Upload Files**, then choose the downloaded `.json` file.

5. The collection will appear in your Postman sidebar.

6. You can now run the API requests, modify the data, and test the Split App backend.

---

## Endpoints Included

- `POST /expenses` – Add a new expense
- `GET /expenses` – List all expenses
- `GET /people` – List all people
- `GET /balances` – Show balances per person
- `GET /settlements` – Show who owes whom
- `PUT /expenses/{id}` – Update an expense by ID
- `DELETE /expenses/{id}` – Delete an expense by ID

---

## Notes

- Make sure your backend API is running locally at `http://127.0.0.1:8000`
- Adjust request data as needed for testing

---

Feel free to contribute or report issues!

