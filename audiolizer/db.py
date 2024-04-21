import os

import pymongo
from pymongo.errors import DuplicateKeyError

client = pymongo.MongoClient(f"mongodb://{os.environ['MONGO_INITDB_ROOT_USERNAME']}:{os.environ['MONGO_INITDB_ROOT_PASSWORD']}@mongo:27017/audiolizer?authSource=admin")

# Database for user accounts
user_db = client.user_accounts
users = user_db.accounts  # User data in 'accounts' collection

try:
	users.create_index([("email", pymongo.ASCENDING)], unique=True)
	users.create_index([("username", pymongo.ASCENDING)], unique=True)
except DuplicateKeyError:
	print('cannot create a unique index -- duplicate keys!')

# Database for application data
app_db = client.app_data  # 'app_data' can be the name of your application database
settings = app_db.settings  # Example collection for app settings
logs = app_db.logs  # Example collection for logging app events


def update_password_hash(username, new_hash):
    user = users.find_one({"username": username})
    if user:
        current_hash = user.get('hashed_password')
        print(f"Current hash: {current_hash}")
        print(f"New hash to apply: {new_hash}")
        if current_hash == new_hash:
            print("No update needed; password hash unchanged.")
            return False
        else:
            result = users.update_one({"username": username}, {"$set": {"hashed_password": new_hash}})
            if result.modified_count > 0:
                print("Password hash updated successfully")
                return True
            else:
                print("Failed to update password hash")
                return False
    else:
        print("No user found")
        return False


def authenticate_user(username, userpass, force_hash_update=False):
    user = users.find_one({"username": username})

    if user is None:
        print(f'could not find {username}')
        return False
    
    stored_hash = user['hashed_password']
    try:
        # Verify provided password against the stored hash
        if ph.verify(stored_hash, userpass):
            # Check if the hash was created with older parameters
            if force_hash_update:
                print('forcing hash update')
            if ph.check_needs_rehash(stored_hash) or force_hash_update:
                # Rehash the password with current settings and store the new hash
                new_hash = ph.hash(userpass)
                update_password_hash(username, new_hash)
            # Proceed with authentication success logic
            return True
    except VerifyMismatchError:
        # Handle incorrect password scenario
        print('incorrect password')
        return False
