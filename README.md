## How to Run
Start the application by running `app.py`.

## Instructions for Testing
1. Hover over the profile and log in as an existing user.
   - Existing users with example data:
     - Username: elza, Password: 12345
     - Username: nora, Password: 12345
2. Enable dark mode by clicking the toggle in the header.
3. From the search bar in the header, search for "chair" or any other item you would like to buy.
4. Select a desired quantity and click "Add to Cart".
5. Click on the icon in the top left corner, click on another item, and add it to cart.
6. Go to your cart and remove the sofa item.
7. Click "Checkout" then "Purchase".
8. Go to your profile and observe your transactions displayed, as well as your bio, address, and phone details.
9. Click "Edit profile" and edit the respective fields as you wish.
10. Go to the order history and search for an item you ordered.
11. From the header, click "New AD".
12. Insert the desired title, description, price, and image. Title and price are required. Click "Upload" when done.
13. Sort by "Yours" to see all your ADs.
14. Put the sort back to "All".
15. Log out and register a new user. This is done by clicking "register here" from the login page.
16. Search for the title of the AD you posted on the elza account and click it.
17. At the bottom of the AD, click on the seller.
18. Observe their profile info and transaction history.
19. From the index page, sort by "Yours" and observe your example ADs.
20. Go to your own profile and click "Delete Account" at the bottom.
21. Log back in as elza and observe that everything from the other account is deleted.
<br/><br/>

------
<br/><br/>
# List of all functionality
<br/><br/>

### Login/register
>- The database table users stores user_id, username, password hash, time of creation, bio, adress, phone number.
>
> #### Register as a new user
> - Username and password require atleast 4 and 5 characters respectivly. This is validated by JS and the server. Using AJAX it checks if the username is already taken, if it is not, then green text stating that the name is available will appear. If the validation fails, an error in red text appears and tells you what is wrong. Once the user tries to register, the server does a last validation before creating the user. The username, password in hash-form, the time the user is created at and the user-id is then saved in the database. 
> - When creating a password, the user has to write it two times, and if the passwords dont match, there is red text telling the user that they dont match. 
> - The user is automatically logged in when the user is created.
> <br/><br/>
>
> #### Login as an existing user
> - Error is displayed when there are empty fields, and if they are empty then the button for login is disabled and a error-message appears. The username and password is validated on the server-side, and if everything is correct, then it adds the user-id to the session. If not, an error message that says "Invalid login credentials"

<br/><br/>

## Products
>- The database table "items" stores item_id, title, description, price and owner_id. The table "images" stores the image path, display order and the product-id the images are for.
>
>### Viewing listed products
>- You can view products through the index-page and through searching for products using the search feature.
>- The index-page shows a grid of products where each product has an image of the product (or a placeholder image if there is no images for the product), the title and the price of the product. The search-bar shows the same information. 
>- The search bar uses ajax to show the user products that match with the search, which show up in a drop-down with clickable elements.
>- On the product page the user can cycle through pictures using the arrows on the sides, view the amount of pictures, see all the information about the products and add a choosen amount of the product to the cart. This can only be done if the user is logged in.
><br/><br/>
>
>### Creating new product
>- Only logged-in users can access this page.
>- There are three input boxes, one for title, one for description and one for price. There is also a "add image button" and a upload button to submit the form
>- The title has a maximum character limit of 22 characters
>- The description input is a span-element with the role "textbox". This has a maximum character limit of 500 characters. Error will be displayed if the user has too many characters. The textvalue is fetched through JS.
>- The price input is a numerical input
>- The image input button works as a input element where you can add multiple images at a time. When uploading images, the images get appended to an array in JS with all the imagefiles so that we can append them to the formData when uploading the product. This enables the user to use the button multiple times without loosing the old files.
>- When images are uploaded, they show up in a grid-like manner, where the image-file is turned into a URL. The order that the images are shown, determine the order of the images in the final product where the first image is the one the user sees in the index. The image-previews have arrows to choose the order, and a button to remove the image.
>- The upload button is disabled until the product has a title and a price. If there is no image, it will use a stock-image for the product. 
>- When the product is being uploaded, a new formData is created in JS. The images and the text all get appended to this formData for further validation on the backend This is done through AJAX.
>- When the formData is sent to the backend, the text-inputs get validated and the images are handled. The image-path, and the image file is created, where the image-path and order is saved to the database, and the image is saved in the images folder. The item's creator is determined by the current logged in users id. 
><br/><br/>
>
>### Deleting product
>- When on a product-page the current user has created, the button "delete-product" appears. This prompts a confirmation pop-up that asks if the user wants to delete the product. If the user presses yes, and everything works, the product gets permanently deleted and the message "product successfully deleted" is shown on the screen with a time-out that redirects to the index after 3 seconds.
>- The backend gets the current logged in user, (which in itself protects products being deleted by users who shouldnt be able to delete the product), and gets the item from the database. This deletes the item, and also the images from the image table. The image-files also get deleted from the server.

<br/><br/>

## Profile, cart and order-history
>- 



- Enable dark mode

- Add items to the cart
- Remove items from the cart
- Total cost of cart items updated with ajax
- Proceed to checkout and purchase items
- View transactions and personal details in the profile
- Search for ordered items in the order history

- View seller profile and transaction history
- Edit profile information

- View all advertisements (sorted by "All")
- View user-specific advertisements (sorted by "Yours")

- Delete user account
- Verify that the deleted account's information is no longer accessible

<br></br>

## Database tables used:

### User table
| User_id | username | password         | created_at  | bio           | adress       | phone      |
|---------|----------|------------------|-------------|---------------|--------------|------------|
| 293565  | test     | 2:sha256:2600... | 31 May 2023 | Funny guy     |              | 90957421   |
| 431988  | asdf     | 73faa39965639... | 30 May 2023 |               | Stavanger 29 |            |
| 915324  | woop     | CPuMItKEKdqBd... | 29 May 2023 | dsfsdfsdfsfsf | Hell         | 666 66 666 |

<br></br>

### Items table
| item_id | title      | description                               | price | owner_id |
|---------|------------|-------------------------------------------|-------|----------|
| 1       | Fancy sofa | Beautiful sofa for the whole family       | 1000  | 293565   |
| 2       | Cool chair | Used as a stool as i have no butt         | 500   | 293565   |
| 3       | Table      | A table for two or just for you my friend | 2000  | 653129   |

<br></br>

### Orders table
| order_id | order_date | user_id | product_id | quantity | total_amount |
|----------|------------|---------|------------|----------|--------------|
| 1        | 2023-06-09 | 531596  | 2          | 1        | 500          |
| 2        | 2023-06-09 | 531596  | 3          | 14       | 28000        |
| 3        | 2023-06-09 | 531596  | 1          | 4        | 4000         |

<br></br>

### Images table
| path                                    | displayOrder | product_id |
|-----------------------------------------|--------------|------------|
| /static/Images/ProductImages/stol.jpg   | 1            | 1          |
| /static/Images/ProductImages/sofa.jpeg  | 1            | 2          |
| /static/Images/ProductImages/sofa2.jpeg | 2            | 2          |

<br></br>

### Cart table
| user_id | item_id | title      | description                               | price | image_path                            | quantity |
|---------|---------|------------|-------------------------------------------|-------|---------------------------------------|----------|
| 531596  | 2       | Cool chair | Used as a stool as i have no butt         | 2000  | /static/Images/ProductImages/stol.jpg | 4        |
| 531596  | 1       | Fancy sofa | Beautiful sofa for the whole family       | 3000  | /static/Images/ProductImages/sofa.jpg | 3        |
| 531596  | 3       | Table      | A table for two or just for you my friend | 34000 | /static/Images/ProductImages/bord.jpg | 17       |
