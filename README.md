# django cafe-management-system

```mermaid
flowchart TB

%% --------------------
%% GUEST USER
%% --------------------
Guest[Guest User]

Guest -->|Visit site| MenuBrowse
MenuBrowse[Browse Menu]
MenuBrowse -->|View items and categories| MenuViewOnly
MenuViewOnly -->|Clicks Add to Cart| LoginRequired[Login Required]

%% --------------------
%% AUTHENTICATION
%% --------------------
LoginRequired --> LoginPage[Login Page]

LoginPage -->|Submit credentials| AuthSystem
AuthSystem{Credentials valid}

AuthSystem -->|No| LoginError[Show generic error]
LoginError --> LoginPage

AuthSystem -->|Yes| HomePage[Homepage]

%% --------------------
%% AUTHENTICATED USER
%% --------------------
HomePage --> MenuPage[Menu Page]
MenuPage -->|Select item| ItemDetail[Item Details]
ItemDetail -->|Choose quantity| AddToCart[Add to Cart]

AddToCart --> CartDB[(Cart Database)]
CartDB --> CartView[View Cart]

%% --------------------
%% DISCOUNT FLOW
%% --------------------
CartView -->|Apply Discount| DiscountOptions[Select discount or enter code]
DiscountOptions --> ValidateDiscount{Valid discount}

ValidateDiscount -->|No| DiscountError[Show invalid discount message]
DiscountError --> CartView

ValidateDiscount -->|Yes| ApplyDiscount[Apply discount calculation]
ApplyDiscount --> UpdatedCart[Updated cart totals]

%% --------------------
%% ORDER PLACEMENT
%% --------------------
UpdatedCart -->|Confirm order| CreateOrder[Create Order]

CreateOrder --> OrderRecord[(Order)]
CreateOrder --> OrderItems[(Order Items)]

OrderRecord --> Pending[pending]
Pending -->|Payment confirmed| Paid[paid]

Paid --> OrderComplete[Order Complete]

%% --------------------
%% ORDER HISTORY
%% --------------------
HomePage -->|View orders| OrderHistory[Order History]
OrderHistory --> OrderRecord

%% --------------------
%% ADMIN FLOW
%% --------------------
Admin[Admin User is_staff]

Admin --> AdminLogin[Admin Login]
AdminLogin --> AdminDashboard[Django Admin Dashboard]

AdminDashboard --> DiscountMgmt[Manage Discounts]
DiscountMgmt --> DiscountModel[(Discount Model)]

AdminDashboard --> MenuMgmt[Manage Menu Items]
MenuMgmt --> MenuModel[(MenuItem Model)]
