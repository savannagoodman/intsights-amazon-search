get_amazon_items.py searches the term 'software testing' on amazon website and writes the results from the first four pages.
It then adds an item to the cart, checking that the item was added correctly.

In order to run the script, the chrome webdriver must be installed.
The script takes into account a slow browser when performing actions that might take some time.

The module "page" contains objects for each page on the site that is visited. Each page object has functions that pertain to 
interaction on the page.

Flow:
- chrome browser is opened
- navigates to amazon and searches the term
- extracts all required information from each result on the page
	- if the information is not accessible in the most common place, tries to find it in other ways 
	before returning INFORMATION UNAVAILABLE
	- moves to the next page of results once finished extracting
- writes all information gathered to csv file
- adds item to add to the cart
	- there are a few edge cases here with different options of book formats to add. 
		- tries to add the paperback version (this is the version that corresponds to the price extracted)
		- in some cases, there is a popup advertising kindle
		- when closing popup fails, the item is NOT added to the cart
- confirms that the item is added by checking if the name of the item is in the cart
	- prints the result





