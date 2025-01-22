def validate_credentials(platform, username, password):
    """
    Validate credentials by simulating a login for a given platform.
    Returns True if credentials are valid, False otherwise.
    """
    # Simulated checks for different platforms
    if platform == 'twitter':
        return username == "valid_twitter_user" and password == "valid_password"
    elif platform == 'facebook':
        return username == "valid_facebook_user" and password == "valid_password"
    elif platform == 'instagram':
        return username == "valid_instagram_user" and password == "valid_password"
    elif platform == 'linkedin':
        return username == "valid_linkedin_user" and password == "valid_password"
    elif platform == 'snapchat':
        return username == "valid_snapchat_user" and password == "valid_password"
    else:
        return False
