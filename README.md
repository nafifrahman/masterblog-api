# Masterblog API

A RESTful blog API built with Flask, plus a simple JavaScript frontend to try it out. It was built as part of the GenAI Engineering program at Masterschool.

## Features

- List all posts, with optional sorting by title, content, author or date
- Add a new post (with automatic integer IDs)
- Update an existing post
- Delete a post
- Search posts by title, content, author or date
- Error handling with clear 400 and 404 responses
- Persistent storage in a JSON file (`backend/posts.json`)
- Interactive API documentation with Swagger UI
- Cross-origin requests enabled with Flask-CORS

## Project Structure

```text
masterblog-api/
├── backend/
│   ├── backend_app.py
│   ├── posts.json
│   └── static/
│       └── masterblog.json
└── frontend/
    ├── frontend_app.py
    ├── templates/
    │   └── index.html
    └── static/
        ├── main.js
        └── styles.css
```


## Installation

```bash
git clone https://github.com/nafifrahman/masterblog-api.git
cd masterblog-api
python -m pip install flask flask-cors flask_swagger_ui
```

## Running the App

Start the backend (port 5002):

```bash
python backend/backend_app.py
```

Start the frontend (port 5001) in a second terminal:

```bash
python frontend/frontend_app.py
```

Then open:

- Frontend: http://localhost:5001
- API: http://localhost:5002/api/posts
- Swagger docs: http://localhost:5002/api/docs/

## API Endpoints

| Method | Endpoint | Description | Success | Errors |
|---|---|---|---|---|
| GET | `/api/posts` | List all posts (optional `sort` and `direction`) | 200 | 400 |
| POST | `/api/posts` | Add a post | 201 | 400 |
| PUT | `/api/posts/<id>` | Update a post | 200 | 400, 404 |
| DELETE | `/api/posts/<id>` | Delete a post | 200 | 404 |
| GET | `/api/posts/search` | Search by `title`, `content`, `author` or `date` | 200 | none |

## Post Format

```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "author": "Your Name",
  "date": "2023-06-07"
}
```

- `title` and `content` are required when adding a post.
- `author` defaults to `Anonymous` and `date` defaults to today (format `YYYY-MM-DD`).

## Examples

Sort posts by date, newest first: `GET /api/posts?sort=date&direction=desc`

Search for posts: `GET /api/posts/search?title=flask`

Add a post: `POST /api/posts` with the body `{"title": "Hello", "content": "My first post", "author": "Nafif"}`

## Technologies

Python 3, Flask, Flask-CORS, Flask-Swagger-UI, HTML, CSS and JavaScript (Fetch API)

## Author

Syed Nafifur Rahman
