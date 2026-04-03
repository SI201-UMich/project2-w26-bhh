# SI 201 - Project #2
# Your name: Brett Hafkin
# Your student id: 55774311
# Your email: bhafkin@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# Yes, although minimal, my use of GenAI did align with the goals and guidelines on my GenAI contract. I used it to primarily help me with the structure of this code and explain certain concepts.
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""

# FIX - Function/Test Case

# Use soup method instead of regex to find info - div tags, find out other tags used - string from certain tag

def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

    # Create empty list to store results
    results = []

    # Open HTML file and parse it with Beautiful Soup
    with open(html_path, "r", encoding="utf-8-sig") as f:
        soup = BeautifulSoup(f.read(), "html.parser")


    listings = soup.find_all("div", class_="t1jojoys dir dir-ltr")
    #print(listings)

    listing_list = []

    for listing in listings:
        listing_title = listing.text
        listing_id = listing.get("id")
        listing_id = listing_id.split("_")[1]
        listing_list.append((listing_title, listing_id))
    
    return listing_list

    # pass

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# FIX - Function/Test Case

def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

    # Open and read listing's HTML file
    file_path = f"html_files/listing_{listing_id}.html"
    with open(file_path, "r", encoding="utf-8-sig") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    # Get all text from page to search through


    # Look at the <li> tags for policy numbers
    
    #<li class="f19phm7j dir dir-ltr">Policy number: <span class="ll4r2nl dir dir-ltr">STR-0000051</span></li>

    policy_tag = soup.find_all("li", class_="f19phm7j dir dir-ltr")[0]
    policy_number = policy_tag.text.split(":")[1].strip()
    # Extract policy number - check for Pending/Exempt first, then look for valid formats
    # policy_number = ""
    
    if "Pending" in policy_number:
        policy_number = "Pending"
    elif "Exempt" in policy_number:
        policy_number = "Exempt"
        
    #print(policy_number)

    host_type = soup.find_all("span", class_="_1mhorg9")

    if host_type:
        host_type = "Superhost"
    else:
        host_type = "regular"

    #<h2 tabindex="-1" class="hnwb2pb dir dir-ltr" elementtiming="LCP-target">Hosted by Seth And Alexa</h2>

    host_names = soup.find_all("h2", class_="hnwb2pb dir dir-ltr")

    for hn in host_names:
        pattern = r"Hosted by (.*)"
        if hn.text and re.findall(pattern, hn.text):
            host_name = re.findall(pattern, hn.text)[0]
            break
    
    room_type_html = soup.find_all("div", class_="_tqmy57")[0].text

    if "private" in room_type_html.lower():
        room_type = "Private Room"
    elif "shared" in room_type_html.lower():
        room_type = "Shared Room"
    else:
        room_type = "Entire Room"

    location_rating = 0.0

    location_rating_html = soup.find_all("div", class_="_7pay")

    if len(location_rating_html) > 3:
        lr = location_rating_html[3].get("aria-label")
        pattern = r"(\d\.\d) out of .*"
        location_rating1 = re.findall(pattern, lr)
        if location_rating1:
            location_rating = float(location_rating1[0])
    
    # # Get location rating, default to 0.0 if not found
    # location_rating = 0.0
    # rating_match = re.search(r"Location\s+(\d+\.?\d*)", all_text)
    # if rating_match:
    #     location_rating = float(rating_match.group(1))


    # # location_rating = 0.0
    # # rating_match = re.search(r"Location\s*[:\s]*(\d+\.?\d*)", all_text, re.IGNORECASE)
    # # if rating_match:
    # #     location_rating = float(rating_match.group(1))    

    
    # # Return nested dictionary with all listing dictionaries

    return {
        listing_id: {
            "policy_number": policy_number, #confirmed good
            "host_type": host_type,
            "host_name": host_name,
            "room_type": room_type,
            "location_rating": location_rating
        }
    }

    # pass

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

    # Get all listing titles and IDs from search results
    listings = load_listing_results(html_path)
    
    # Create empty list to store complete listing data
    database = []
    
    # Loop through each listing found in search results
    for title, listing_id in listings:
        # Get all detailed information for specific listing
        details = get_listing_details(listing_id)
        
        # Extract inner dictionary using listing ID as key
        listing_info = details[listing_id]
        
        # Combine all data into tuple in order
        complete_listing = (
            title,                                    
            listing_id,                               
            listing_info["policy_number"],            
            listing_info["host_type"],                
            listing_info["host_name"],                
            listing_info["room_type"],                
            listing_info["location_rating"]
        )
        
        # Add listing's tuple to database
        database.append(complete_listing)
    
    return database

    # pass

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
   
    # Sort listings by location_rating (index 6) from highest to lowest
    sorted_data = sorted(data, key=lambda x: x[6], reverse=True)
    
    # Open CSV file for writing
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        
        # Write the header row with column names
        writer.writerow(["Listing Title", "Listing ID", "Policy Number", "Host Type", "Host Name", "Room Type", "Location Rating"])
        
        # Write each listing as a row in the CSV file
        for row in sorted_data:
            writer.writerow(row)
    
    # pass

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

    # Create dictionaries to store totals and counts for each room type
    total_ratings = {}
    count_ratings = {}
    
    # Loop through each listing
    for listing in data:
        # Get room_type and location_rating - from complete_listing
        room_type = listing[5]
        rating = listing[6]
        
        # Skip listings with no rating
        if rating == 0.0:
            continue
        
        # Add rating to total and increase count for room type
        if room_type in total_ratings:
            total_ratings[room_type] += rating
            count_ratings[room_type] += 1
        else:
            total_ratings[room_type] = rating
            count_ratings[room_type] = 1
    
    # Calculate average for each room type
    averages = {}
    for room_type in total_ratings:
        averages[room_type] = total_ratings[room_type] / count_ratings[room_type]
    
    return averages
    
    # pass

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

    # Create empty list to store invalid listing IDs
    invalid_ids = []
    
    # Loop through each listing in the database
    for listing in data:
        # Get listing_id and policy_number - from complete_listing
        listing_id = listing[1]
        policy_number = listing[2]
        
        # Skip listings that are Pending or Exempt
        if policy_number.lower() == "pending" or policy_number.lower() == "exempt":
            continue
        
        # Check if policy number matches valid format
        match1 = re.search(r"(?:20\d{2}-00\d{4}STR)", policy_number)
        
        # Check if policy number matches valid format
        match2 = re.search(r"(STR-000\d{4})", policy_number)
        
        # If policy number doesn't match either format, add listing_id to invalid list
        if not match1 and not match2:
            invalid_ids.append(listing_id)
    
    return invalid_ids

    # pass

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# DELETE -- OH: Assertion - length of listings, check first two listings equal to "exact something", if return value is required to be dict (assertin - that variable - then dict, assertequal policy numbers - compared to actual policy numbers)

class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.

        self.assertEqual(len(self.listings), 18)

        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").

        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

        # pass

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        details_list = []
        for listing_id in html_list:
            details = get_listing_details(listing_id)
            details_list.append(details)

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        
        self.assertEqual(details_list[0]["467507"]["policy_number"], "STR-0005349")

        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".

        idx = html_list.index("1944564")
        self.assertEqual(details_list[idx]["1944564"]["host_type"], "Superhost")
        self.assertEqual(details_list[idx]["1944564"]["room_type"], "Entire Room")

        # 3) Check that listing 1944564 has the correct location rating 4.9.

        self.assertEqual(details_list[idx]["1944564"]["location_rating"], 4.9)

        # pass

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        for listing in self.detailed_data:
            self.assertEqual(len(listing), 7)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).

        last_tuple = self.detailed_data[-1]
        expected_last = ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
        self.assertEqual(last_tuple, expected_last)

        # pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.

        output_csv(self.detailed_data, out_path)

        # TODO: Read the CSV back in and store rows in a list.

        rows = []
        with open(out_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)

        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].

        expected_first_row = ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"]
        self.assertEqual(rows[1], expected_first_row)

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.

        averages = avg_location_rating_by_room_type(self.detailed_data)

        # TODO: Check that the average for "Private Room" is 4.9.

        self.assertEqual(averages["Private Room"], 4.9)

        # pass

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.

        invalid_listings = validate_policy_numbers(self.detailed_data)

        # TODO: Check that the list contains exactly "16204265" for this dataset.

        self.assertEqual(invalid_listings, ["16204265"])

        # pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)