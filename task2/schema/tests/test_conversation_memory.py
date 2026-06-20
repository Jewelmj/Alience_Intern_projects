from schema.session.conversation_manager import (
    ConversationManager
)
from schema.session.conversation_manager import (
    ConversationManager
)

def test_add_message_stores_history():

    session_id = "test-session"

    ConversationManager.clear_history(
        session_id
    )

    ConversationManager.add_turn(
        session_id,
        "user",
        "Hello"
    )

    ConversationManager.add_turn(
        session_id,
        "assistant",
        "Hi there"
    )

    history = (
        ConversationManager.get_history(
            session_id
        )
    )

    assert len(history) == 2

    assert history[0]["role"] == "user"
    assert history[0]["message"] == "Hello"

    assert history[1]["role"] == "assistant"
    assert history[1]["message"] == "Hi there"

def test_history_is_trimmed():

    session_id = "trim-session"

    ConversationManager.clear_history(
        session_id
    )

    for i in range(12):

        ConversationManager.add_turn(
            session_id,
            "user",
            f"user-{i}"
        )

    history = (
        ConversationManager.get_history(
            session_id
        )
    )

    assert len(history) == 10

    assert history[0]["message"] == "user-2"

def test_sessions_are_isolated():

    ConversationManager.clear_history(
        "session-a"
    )

    ConversationManager.clear_history(
        "session-b"
    )

    ConversationManager.add_turn(
        "session-a",
        "user",
        "hello"
    )

    ConversationManager.add_turn(
        "session-b",
        "user",
        "different"
    )

    history_a = (
        ConversationManager.get_history(
            "session-a"
        )
    )

    history_b = (
        ConversationManager.get_history(
            "session-b"
        )
    )

    assert history_a[0]["message"] == "hello"

    assert history_b[0]["message"] == "different"