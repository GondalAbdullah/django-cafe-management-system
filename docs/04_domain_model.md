# Domain model

This document describes the core data model for the Coffee Shop App.  
The ERD captures entities, attributes, and relationships required to support menu browsing, order placement, and a flexible discount/coupon system.

The design directly follows the project requirements and is optimized for Django ORM implementation.

---

## Core Entities Overview

- User (Django built-in)
- MenuItem
- Discount
- Order
- OrderItem

---

## ERD Diagram

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--o{ ORDER_ITEM : contains
    MENU_ITEM ||--o{ ORDER_ITEM : included_in
    DISCOUNT ||--o{ ORDER : applied_to
    DISCOUNT }o--o{ MENU_ITEM : applies_to

    USER {
        int id PK
        string email
        string password
        boolean is_staff
    }

    MENU_ITEM {
        int id PK
        string name
        text description
        decimal price
        string category
    }

    DISCOUNT {
        int id PK
        string name
        text description
        string type
        decimal value
        decimal min_order_value
        datetime valid_from
        datetime valid_to
        int max_uses
        int max_uses_per_customer
        boolean is_active
    }

    ORDER {
        int id PK
        decimal total_before_discount
        decimal discount_amount
        decimal total_after_discount
        datetime order_date
        string status
    }

    ORDER_ITEM {
        int id PK
        int quantity
        decimal price
    }
```
