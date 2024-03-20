def imdb_top_content(num_results,content_type):

    import random
    import requests
    from bs4 import BeautifulSoup
    import re
    import current_date_formatted

    today = current_date_formatted.get_current_date()
    current_year = current_date_formatted.get_current_year()
    today_till_year_end = f"{today},{current_year}-12-31"
    url = f"https://m.imdb.com/search/title/?title_type={content_type}&release_date={today_till_year_end}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    # Send an HTTP GET request to the URL
    response = requests.get(url=url, headers=headers)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Find all elements with class "ipc-metadata-list-summary-item sc-59b6048d-0 cuaJSp cli-parent"
        summary_items = soup.find_all(class_="ipc-metadata-list-summary-item")

        # Initialize lists to store the extracted information
        list_of_titles = []
        list_of_sources = []
        list_of_descriptions = []

        # Loop through each summary item
        for summary_item in summary_items:

            try:
                text_box = summary_item.find('h3', class_='ipc-title__text').text
                text_box = re.sub('^[0-9]+\.\s*', '', text_box)
                list_of_titles.append(text_box)
            except:
                list_of_titles.append(('No Title available yet.'))

            try:
                description = summary_item.find(class_='ipc-html-content-inner-div').text
                list_of_descriptions.append(description)
            except:
                list_of_descriptions.append('No description available yet.')

            try:
                image_container = summary_item.find(class_="ipc-image")
                srcset_attribute = image_container.get('srcset')
                all_sources = srcset_attribute.split(sep=',')

                if all_sources[-4]:
                    list_of_sources.append(all_sources[-4])
                else:
                    list_of_sources.append(all_sources[0])
            except:

                list_of_sources.append('https://www.distefanosales.com/wp-content/uploads/2023/08/image-coming-soon-placeholder.png')

        combined_lists = list(zip(list_of_titles, list_of_sources, list_of_descriptions))

        random.shuffle(combined_lists)

        combined_lists = combined_lists[:num_results]

        return combined_lists
    except:

        return []