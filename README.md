# Final-Project-Python
## Runescape Shopping Cart
#### Description:
My project is a shopping cart based on the game Old School Runescape. It takes the cost of items inputted from the Old School Runescape Wiki, which is taken from the Grand Exchange(in game Runescape trading hub), asks for quantity and then calculates the total cost, printing out the items, the total cost of the individual items bought and then the total cost overall at the bottom, like a receipt. It then stores the the purchase history in storage.csv and backup_storage.csv. The user can then choose to continue shopping or end it, which will then show the final receipt.
Also have a test_project.py, which tests all important functions.

For this project, when I had initially looked into webscraping, I was initially going to use beautifulsoup, the one thats currently being used.  However, beautifulsoup doesnt deal with dynamic webscraping. I tried to learn scrapy, a framework designed for web scraping and webcrawling, but in the end I chose beautifulsoup, mainly because I found that Runescape wiki had partnered up with Runelite, so all Grand Exchange prices on the wiki are real time with the game. This meant I would not need to use the official website as the wiki gets it straight from the game.

Another dilemma was what to store my data in. I ended up choosing csv, mainly because I was most comfortable with the library, but also because its easily readable, which is important since you can have so much data that you will need to sift through if necessary.

For future updates, Im planning to add a login system and search bar for when you want to search for items.
