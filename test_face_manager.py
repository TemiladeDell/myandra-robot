from face_manager import identify_user
from user_manager import find_user_profile

user_id = identify_user()

if user_id:

    profile = find_user_profile(user_id)

    print(
        f"Welcome back {profile['name']}"
    )

else:

    print(
        "Unknown User"
    )
