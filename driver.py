import requests

class Driver:
    base_url = None
    username = None
    password = None
    headers = {"Content-Type": "application/json"}
    
    userId = None
    teamId = None
    
    def __init__(self, base_url):
        self.base_url = base_url + '/api/v4/'
        
    def login(self, username, password):
        """
        Login to the server.

        Args:
            username (str): Username
            password (str): Password
        """
        url = self.base_url + 'users/login'
        payload = {
            'login_id'  : username,
            'password'  : password
        }
    
        response = requests.post(url, json=payload, headers=self.headers)
        token = response.headers.get("token")
        self.headers["Authorization"] = f"Bearer {token}"
        self.userId = response.json().get('id')
    
    def list_teams(self):
        """
        Return a list of all available teams.

        Returns:
            dict: Available teams
        """
        url = self.base_url + 'teams'
        response = requests.get(url, headers = self.headers)
        return response.json()
    
    def enter_team(self, teamId):
        """
        Enter team based on its id.

        Args:
            teamname (str): team id.
        """
        self.teamId = teamId
        
    def search_posts(self, str):
        """
        Search all visible posts for a certain string.

        Args:
            str (str): Part of the post

        Returns:
            list(str): List of post ids that contain str in some order (but unclear what order).
        """
        url = self.base_url + "teams/" + self.teamId + '/posts/search'
        payload = {
            'terms' : str,
            'is_or_search' : False
        }
        response = requests.post(url, headers = self.headers, json = payload)
        return response.json()['order']
    
    def get_post(self, postId):
        """
        Get dict representation of the post.

        Args:
            postId (str): Post id

        Returns:
            dict: All fields in the post object.
        """
        url = self.base_url + 'posts/' + postId
        response = requests.get(url, headers = self.headers)
        return response.json()
    
    def get_name(self, userId):
        """

        Get a user's first and last names.
        
        Args:
            userId (str): user ID

        Returns:
            str: first_name last_name
        """
        url = self.base_url + 'users/ids'
        payload = [userId]
        response = requests.post(url, headers = self.headers, json = payload)
        name = response.json()[0].get('first_name') + ' ' + response.json()[0].get('last_name')
        return name
        
    def react(self, postId, emoji):
        """
        React to a postId with the emoji name.

        Args:
            postId (str): Post id
            emoji (str): Emoji name

        Returns:
            str: Status code from API call
        """
        url = self.base_url + 'reactions'
        payload = {
            'post_id' : postId,
            'user_id' : self.userId,
            'emoji_name' : emoji
        }
        response = requests.post(url, headers = self.headers, json = payload)
        return response.status_code