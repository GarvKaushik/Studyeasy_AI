import time


sessions = {}


SESSION_EXPIRY_SECONDS = 3600


def create_session(session_id):

    sessions[session_id] = {
        "created_at": time.time(),
        "last_accessed": time.time()
    }


def update_session_access(session_id):

    if session_id in sessions:
        sessions[session_id]["last_accessed"] = time.time()


def is_session_expired(session_id):

    if session_id not in sessions:
        return True

    last_accessed = sessions[session_id]["last_accessed"]

    return (
        time.time() - last_accessed
        > SESSION_EXPIRY_SECONDS
    )


def delete_session(session_id):

    if session_id in sessions:
        del sessions[session_id]