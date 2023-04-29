# Web Application Requirements

This is our plan for the web-project. There are also pictures of how the page layout is supposed to be in the folder **PageIdea**

## What does the application do?

- The platform combines a webshop and a trading platform where users can buy and sell listed items from each other.
- Visitors can browse the website without any restriction, but need to create an account or log in if they intend to buy or sell an item.
- After registration or login, users can create listings of their items, buy items listed by other users, and enjoy the full functionality of the platform.
- The platform includes features such as a search bar to filter items by name, category, or price range, and the ability to rate and leave feedback on users or items.

## What data is stored in files/database?

- Data for the platform will be stored in an SQLite database, with two tables representing the users and items.
- Each user will have a unique username, email address, and password, while items will have a name, description, price, and a reference to the user who created the listing.

## Initial layout for your page

- The layout will be implemented using HTML and CSS.
- The platform will have a home page that displays the most popular or recently added items, a page for browsing categories of items, and a page for creating listings.
- AJAX calls will be used to facilitate interaction with the database, such as adding or updating listings.

## Possible extra functionality

- Enable users to send each other messages
- Give each product a basic rating system
- Give users the ability to customize the color on the page (e.g. dark-mode)
- Have the page support multiple types of currency
- Implement a payment system.
- Implement a feature to allow users to create wishlists.
