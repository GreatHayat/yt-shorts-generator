import os
import time
import mimetypes
import requests


def download_image(url, filename, max_retries=3, retry_delay=1):
    retries = 0
    while retries < max_retries:
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            print(f'{retries} try')
            # Check if the request was successful
            if response.status_code == 200:
                # Get the Content-Type header from the response
                content_type = response.headers.get('Content-Type')

                # Determine the file extension based on the Content-Type
                extension = mimetypes.guess_extension(content_type)

                # Append the extension to the provided filename
                filename_with_extension = f"{filename}{extension}"

                # Create a directory to save the image (if it doesn't exist)
                os.makedirs('images', exist_ok=True)

                # Open a file in binary write mode
                with open(os.path.join('images', filename_with_extension), 'wb') as file:
                    # Write the content of the response to the file
                    file.write(response.content)

                print(
                    f"Image '{filename_with_extension}' downloaded successfully.")
                return

            else:
                print(f"Failed to download image. Status code: {
                      response.status_code}")
                retries += 1
                time.sleep(retry_delay)

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while downloading image: {e}")
            retries += 1
            time.sleep(retry_delay)

    print(f"Failed to download image after {max_retries} retries.")


