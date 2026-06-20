from collections import defaultdict

MAX_HISTORY = 5

class ConversationManager:
    _history = defaultdict(list)
    
    @classmethod
    def add_turn(cls,session_id,role,message):
        cls._history[session_id].append(
            {
                "role": role,
                "message": message
            }
        )

        cls._history[session_id] = (
            cls._history[session_id]
            [-MAX_HISTORY * 2:]
        )

    @classmethod
    def get_history(cls,session_id):
        return cls._history.get(session_id,[])

    @classmethod
    def clear_history(cls,session_id):
        cls._history.pop(session_id,None)