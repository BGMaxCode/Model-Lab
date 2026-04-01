# Flask + Bootstrap Management System - Minimal Setup

Generate a complete, working Flask management/registration system with **5 files only**. Use **Bootstrap 5** for styling.

## Simple File Structure

```
project/
├── app.py
├── templates/
│   ├── base.html
│   ├── auth.html
│   ├── dashboard.html
│   ├── items.html
│   └── form.html
└── requirements.txt
```

That's it. **No subdirectories**, **no component includes**, **no separate admin/management/auth folders**.

---

## Files to Generate

### 1. `app.py`
- Flask app initialization
- User model: id, name, email, password_hash, created_at
- Item model: id, name, email, category, description, status, created_at, user_id
- Routes:
  - `GET/POST /register` → auth.html
  - `GET/POST /login` → auth.html
  - `GET /logout` → clear session
  - `GET /dashboard` → dashboard.html (protected)
  - `GET /items` → items.html (protected)
  - `POST /items` → create item
  - `GET /items/<id>` → show item
  - `POST /items/<id>` → update item
  - `DELETE /items/<id>` → delete item
- Session-based authentication
- Password hashing (werkzeug.security)
- Flash messages for user feedback
- Simple in-memory or SQLite database
- Error handlers (404, 500)

### 2. `base.html`
- Navigation bar with:
  - Site name/logo left
  - Dashboard, Items links (if logged in)
  - Logout button (if logged in)
  - Login/Register links (if not logged in)
  - Hamburger menu for mobile
- Flash messages container at top
- `{% block content %}` for child templates
- Footer
- Bootstrap 5 CDN links
- Viewport meta tag for responsive design

### 3. `auth.html`
- Two sections: Login and Register (use tabs or simple toggle)
- **Login:**
  - Email input
  - Password input
  - Remember me checkbox
  - Submit button
  - Link to register
- **Register:**
  - Full name input
  - Email input
  - Password input
  - Confirm password input
  - Terms checkbox
  - Submit button
  - Link to login
- Both forms in centered card layout
- Form validation feedback
- CSRF tokens in both forms

### 4. `dashboard.html`
- Welcome greeting with user's name
- 4 stat cards (Name, Total Items, Active Items, Inactive Items) with icons
- Recent items table with columns: Name, Category, Status (badge), Created Date, Actions
- "Add New Item" button
- View/Edit/Delete action buttons per row
- Simple pagination
- Responsive grid layout

### 5. `items.html`
- Page title "Items Management"
- "Add New Item" button at top
- Search input for filtering
- Sortable table with columns: Name, Email, Category, Status (badge), Date, Actions
- Status badges (green=active, red=inactive)
- Edit and Delete icons/buttons per row
- Pagination controls
- Empty state message if no items
- Responsive table

### 6. `form.html` (Create/Edit Item)
- Page title: "Create New Item" or "Edit Item"
- Form fields:
  - Name (text, required)
  - Email (email, required)
  - Category (dropdown: Electronics, Books, Furniture, Other)
  - Description (textarea, optional)
  - Status (radio: Active/Inactive, default Active)
  - File upload (optional)
- Required field indicators (*)
- Validation feedback
- Save button
- Cancel button (back to items)
- CSRF token

---

## Design Requirements
- **Bootstrap 5 only** (no custom CSS files)
- **Bootstrap Icons** via CDN for buttons
- Professional, clean design
- Responsive (mobile/tablet/desktop)
- Status badges in Bootstrap colors
- Form validation feedback
- Hover effects on buttons/tables

## Routes Summary
```
GET/POST /register           → auth.html
GET/POST /login              → auth.html
GET      /logout             → redirect to login
GET      /dashboard          → dashboard.html (protected)
GET      /items              → items.html (protected)
GET      /items/new          → form.html (protected)
POST     /items              → create item
GET      /items/<id>         → show item
POST     /items/<id>         → update item
DELETE   /items/<id>         → delete item
```

## Requirements
- Use Flask
- Use in-memory or simple SQLite database
- Session-based auth (no JWT)
- Bootstrap 5 CDN
- Bootstrap Icons CDN
- Password hashing
- CSRF protection
- Flash messages

---

**That's all. Keep it simple.**
