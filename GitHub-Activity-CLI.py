import json
import sys
import urllib.request #Used as this is a lightweight project and is apart of pythons standard library

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return data
            else: 
                print("Error: Unable to fetch data.")
                return 
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    return

def get_activity(data):
    activity_list = []
    for event in data[:10]:
        eventType = event["type"]
        eventRepo = event["repo"]["name"]

        if eventType == "CreateEvent":
            ref_type = event["payload"]["ref_type"]
            activity_list.append(f"Created a git {ref_type}, Repository: {eventRepo}")

        elif eventType == "DeleteEvent":
            ref_type = event["payload"]["ref_type"]
            activity_list.append(f"Deleted a git {ref_type}, Repository: {eventRepo}")

        elif eventType == "ForkEvent":
            activity_list.append(f"Forked {eventRepo}")

        elif eventType == "IssuesEvent":
            action = event["payload"]["action"]
            activity_list.append(f"{action} an issue in {eventRepo}")

        elif eventType == "MemberEvent":
            member = event["payload"]["member"]
            activity_list.append(f"Added {member} to Repository: {eventRepo}")

        elif eventType == "PullRequestEvent":
            action = event["payload"]["action"]
            activity_list.append(f"{action} a pull request in {eventRepo}")

        elif eventType == "PushEvent":
            commits = len(event["payload"].get("commits", []))
            activity_list.append(f"Pushed {commits} commits to {eventRepo}")

        elif eventType == "WatchEvent":
            activity_list.append(f"Starred {eventRepo}")
    
    return activity_list

def main():
    if len(sys.argv) != 2:
        print("Usage: github-activity <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    events = fetch_github_activity(username)

    if events:
        activities = get_activity(events)
        if activities:
            print("Recent Activity:")
            for activity in activities:
                print(f"- {activity}")
        else:
            print("No recent activity")
    else: 
        print("Failed to fetch activity: Invalid username")

if __name__ == "__main__":
    main()