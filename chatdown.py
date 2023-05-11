import os
import sys
import requests
import json
import time


def download_chat_logs(video_id):
    total_comments = 0
    offset = 0
    offset_increment = 160

    combined_file_path = f"chatlog_for_{video_id}.json"

    print("Downloading chat logs...")
    previous_data = None
    with open(combined_file_path, "w") as combined_file:
        while True:
            url = f"https://chatreplay.stream/api/videos/{video_id}/comments?offset={offset}"
            response = requests.get(url)
            data = response.json()

            comments = data["comments"]
            if not comments or data == previous_data:
                break

            # Save each comment to the combined JSON file
            for comment in comments:
                # Write comment as a line in the combined file
                json.dump(comment, combined_file)
                combined_file.write("\n")

                total_comments += 1

                # Echo the contents of the downloaded comment
                comment_content = comment.get("message", "")
                print(f"Downloaded comment: {comment_content}")

            offset += offset_increment
            time.sleep(0.5)  # Add a delay to avoid overwhelming the server

            # Update the previous_data with the current data
            previous_data = data

    if total_comments > 0:
        print(f"Downloaded {total_comments} chat logs.")
        print(f"Combined JSON file saved at {combined_file_path}.")
    else:
        print("No chat logs found for the specified video.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatdown.py [video_id]")
        print("Example: python chatdown.py OXe1ff8MzyU")
    else:
        video_id = sys.argv[1]
        download_chat_logs(video_id)
