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

------

## List of all functionality

### Login/register

> #### Register as a new user
> - Username and password require atleast 4 and 5 characters respectivly. This is validated by JS and the server. Using AJAX it checks if the username is already taken. If the validation fails, an error in red text appears and tells you what is wrong. Once the user tries to register, the server does a last validation before creating the user. The username, password in hash-form, the time the user is created at and the user-id is then saved in the database. 
> - The user is automatically logged in when the user is created.
> ---
> #### Login as an existing user
> - Error is displayed when there are empty fields, and if they are empty then the button for login is disabled and a error-message appears. The username and password is validated on the server-side, and if everything is correct, then it adds the user-id to the session. If not, an error message that says "Invalid login credentials"




- Enable dark mode
- Search for items in the header search bar
- Add items to the cart
- Remove items from the cart
- Total cost of cart items updated with ajax
- Proceed to checkout and purchase items
- View transactions and personal details in the profile
- Edit profile information
- Search for ordered items in the order history
- Upload and remove image(s) when creating new AD
- Swich order of the images
- Post a new advertisement
- View all advertisements (sorted by "All")
- View user-specific advertisements (sorted by "Yours")
- Click on an advertisement to view details
- Shuffle through images from an advertisment
- View seller profile and transaction history
- Delete user account
- Verify that the deleted account's information is no longer accessible
