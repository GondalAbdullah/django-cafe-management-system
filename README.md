# Coffee Shop Management App

A Django-based web application for a coffee shop that supports menu browsing, cart-based ordering, and a flexible discount/coupon engine. Built to handle real-world discount logic — percentage, fixed-amount, and item-specific discounts — with usage limits and validity windows.

## Features

- **User Authentication** — customer registration, login/logout, and staff (admin) accounts via Django's built-in User model
- **Menu Browsing** — public menu view grouped by category (Coffee, Pastry, Drink, Other), with category filtering
- **Cart & Ordering** — authenticated customers can add/remove items, view running totals, and place orders
- **Discount Engine** — supports three discount types:
  - Percentage off total order
  - Fixed amount off total order
  - Item-specific discounts (applies only to selected menu items)
- **Discount Validation** — checks active status, valid date range, minimum order value, and total/per-customer usage limits before applying
- **Order History** — customers can view past orders with pre-discount total, applied discount, discount amount, and final total
- **Admin Dashboard** — Django admin interface for managing menu items, discounts, and viewing all orders

## Tech Stack

- **Backend:** Django, Django REST Framework (if API endpoints are exposed)
- **Database:** PostgreSQL / SQLite (dev)
- **Auth:** Django built-in authentication

## Data Models

| Model | Purpose |
|---|---|
| `User` | Built-in Django user, extended with `is_staff` for admin access |
| `MenuItem` | Name, description, price, category |
| `Discount` | Type (percentage/fixed/item-specific), value, conditions, usage limits, active window |
| `Order` | Customer, totals before/after discount, applied discount, status |
| `OrderItem` | Line items linking an order to a menu item, quantity, and price at time of order |

## Discount Calculation Logic

- **Percentage:** `discount_amount = total_before_discount * (value / 100)`
- **Fixed:** `discount_amount = min(value, total_before_discount)`
- **Item-specific:** sum of `(item_price * quantity * (value / 100))` across eligible items

Only one discount can be applied per order.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register/` | Register a new user |
| POST | `/login/` | Log in |
| POST | `/logout/` | Log out |
| GET | `/menu/` | List menu items (optional `?category=`) |
| GET | `/menu/<id>/` | Menu item detail |
| GET | `/cart/` | View current cart |
| POST | `/cart/add/` | Add item to cart |
| POST | `/cart/remove/` | Remove item from cart |
| POST | `/cart/apply_discount/` | Apply a discount to the cart |
| POST | `/orders/` | Place an order |
| GET | `/orders/` | List orders for current user |
| GET | `/orders/<id>/` | Order detail |

## Setup

1. Clone the repository
```bash
   git clone <repo-url>
   cd coffee-shop-app
```
2. Create a virtual environment and install dependencies
```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```
3. Apply migrations
```bash
   python manage.py migrate
```
4. Create a superuser (for admin access)
```bash
   python manage.py createsuperuser
```
5. Run the development server
```bash
   python manage.py runserver
```

## Notes

- All state-changing endpoints require CSRF tokens and authentication.
- Discount usage is tracked against `Order` records to enforce `max_uses` and `max_uses_per_customer`.
- Payment processing is assumed to be handled externally; the app only tracks order status (`pending`, `paid`, `completed`, `canceled`).

## License

MIT
