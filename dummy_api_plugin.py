from plugin import Plugin
import requests
import json
from settings import dummyApiToken


class DummyApiPlugin(Plugin):

    def connectivity_test(self):
        # minimum limit is 5
        dummy_api_connectivity_test_url = "https://dummyapi.io/data/v1/user?limit=5"

        headers = {"app-id": dummyApiToken}

        response = requests.get(
            dummy_api_connectivity_test_url, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            return True
        else:
            error_json = response.json()
            error_massage = error_json["error"]
            print(
                f"API call failed with error massage: {error_massage} and status code: {response.status_code}")
            return False

    def collect(self):
        url = "https://dummyapi.io/data/v1"
        users_url = f"{url}/user"
        posts_url = f"{url}/post"
        comments_url = f"{url}/post/{{post_id}}/comment"

        headers = {"app-id": dummyApiToken}

        users = []
        posts = []

        # User's collection
        page = 0
        while True:
            response = requests.get(
                users_url, headers=headers, params={"page": page})

            if response.status_code == 200:
                response_json = response.json()
                users += response_json["data"]

                if response_json["page"] == response_json["total"]:
                    # reached the last page, break out of loop
                    break
                else:
                    # increment page number and continue fetching
                    page += 1
            else:
                error_json = response.json()
                error_massage = error_json["error"]
                print(
                    f"API call failed with error massage: {error_massage} and status code: {response.status_code}")
                break

        # Save evidence of users to file
        with open('users.json', 'w') as f:
            json.dump(users, f)

        # Post's collection
        response = requests.get(
            posts_url, headers=headers, params={"limit": 50})

        if response.status_code == 200:
            response_json = response.json()
            posts = response_json["data"]
        else:
            error_json = response.json()
            error_massage = error_json["error"]
            print(
                f"API call failed with error massage: {error_massage} and status code: {response.status_code}")

        # Fetch comments for each post
        for post in posts:
            post_id = post["id"]
            response = requests.get(comments_url.format(
                post_id=post_id), headers=headers)

            if response.status_code == 200:
                response_json = response.json()
                post["comments"] = response_json["data"]
            else:
                error_json = response.json()
                error_massage = error_json["error"]
                print(
                    f"API call failed with error massage: {error_massage} and status code: {response.status_code}")

        # Save evidence of posts to file
        with open('posts.json', 'w') as f:
            json.dump(posts, f)
