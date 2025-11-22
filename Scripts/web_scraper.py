import requests # Allows us to send requests (like a web browser) to get HTML content
from bs4 import BeautifulSoup # The parser; turns raw HTML into a searchable Python object ('the soup')
import csv # The tool we need to easily save data into a structured CSV file 

# 1. Define the URL of the wbsite we want to scrape
URL = "https://books.toscrape.com/" # A great practice website for scraping

# 2. Make the HTTP GET request 
# This will fetch the content of the webpage
# The result is stored in the 'response' object
response = requests.get(URL)

# 3. Check if the request was successful
# A status code of 200 means success
if response.status_code == 200:
    print("Success! Status code 200. Proceeding to parse the content...")
    # 4. Print the content of the webpage
    # The raw HTML content is stored in response.text
    # We will use this in later steps 
    raw_html = response.text
    
    # Create the BeautifulSoup object(the "soup")
    # This allows us to navigate and search the HTML structure easily
    soup = BeautifulSoup(raw_html, 'html.parser')

    # Test line: Finds the <title> tag and prints its text content to confirm parsing worked 
    page_title = soup.title.get_text()
    print(f"\nSuccessfully parsed the page! Title: {page_title}")

    # Use find_all() to get a Python List of all book containers 
    # Find_all() searches the entire page for all elements that match the criteria
    # We target the <article> tag with the class 'product_pod', as this container  holds All the data for one  single book(title, price, image, etc.)
    all_books = soup.find_all('article', class_='product_pod')
    print(f"\nFound {len(all_books)} books on the page.")
    
    # This empty list will store all the Title and Price data as we loop through the books. 
    book_list = []

    # Start the loop: we iterate through every book container we found in 'all_books'.
    for book in all_books:
        # Inside this loop, 'book'  is now the container for ONE specific book
        
        # Extract the title
        # We find the <h3> tag,  then the <a> tag inside it, then grab the value of the 'title' attribute
        # This is robust because we chaining finds within the small 'book' container. 
        title_tag = book.find('h3').find('a')
        title = title_tag['title'] # The title text is stored in the 'title' attribute. 

        # Extract the price
        # We find the <p> tag with the class 'price_color', which holds the price text.
        price_tag = book.find('p', class_='price_color')
        price = price_tag.get_text() # .get_text() extracts the human-readable text (e.g., '£51.77').

        # Store the data: We add a Python dictionary containing the Title and Price to our main 'book_list'.
        book_list.append({'Title': title, 'Price': price})

    # We move outside the loop now, after all books have been processed.
    # We move the print statements outside the loop to avoid excessive output or so they only run once.    
    print("\n--- Extracted Titles and Prices(First 5 books) ---")
    for item in book_list[:5]: # Print only the first 5 books for brevity
        print(f"Title: {item['Title']}, Price: {item['Price']}")   

    # Save the data to a CSV file
    csv_file_name = 'books.csv'
    # We define the column headers for the CSV.These must match the dictionary keys used above('Title', 'Price').
    fieldnames = ['Title', 'Price']
    try:
        # 'with open(...)' opens the file, and automatically closes it when done(safer!)
        # 'w' means write mode (will overwrite existing file or create new). newline=='' prevents extra blank lines.
        with open(csv_file_name,'w', newline='', encoding='utf-8') as csvfile:
            # csv.Dictwriter knows how to write data from a list of dictionaries.
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
            # Write the header row (Title, Price) at the top of the file.
            writer.writeheader()
            # Write all the dictionaries stored in our book_list to the CSV file.
            writer.writerows(book_list)
        print(f"\nData successfully saved to {csv_file_name}")
    except IOError:
        # A basic error check in case the script can't access the folder to write the file.
        print("Error: Could not write to file. Check your file permissions.")

# If the initial request failed, print an error message with the status code.        
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    
