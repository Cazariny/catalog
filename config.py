class Auth:
    """
    Auth class contains details for flow used in OAuth authentication
    using Google
    """
    # OAuth credentials
    CLIENT_ID = '900234952643-va0na2ga3p7b0qivtjeaqkijcpnv9to5.apps.googleusercontent.com'
    CLIENT_SECRET = '9DILVZpTqT8mDIqYXX0ukkg1'
    # URI that google server will redirect to
    REDIRECT_URI = 'http://localhost:5000/gconnect'
    # Endpoint to start OAuth request from
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    # Endpoint to fetch user token
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    # Endpoint to get user information at the end of oauth
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    # Data we plan to access from Google profile
    SCOPE = ['profile', 'email']