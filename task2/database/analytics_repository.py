from database.connection import db

class AnalyticsRepository:
    def __init__(self):
        self.collection = (
            db.analytics
        )

    def save(self,record: dict):
        result = (
            self.collection.insert_one(
                record
            )
        )

        return str(result.inserted_id)

    def get_by_id(self,interaction_id: str):

        return (
            self.collection.find_one(
                {
                    "interaction_id":
                    interaction_id
                }
            )
        )

    def update_feedback(self,interaction_id: str,feedback: str):

        return (
            self.collection.update_one(
                {
                    "interaction_id":
                    interaction_id
                },
                {
                    "$set": {
                        "feedback":
                        feedback
                    }
                }
            )
        )
    
    def get_all(self):
        return list(self.collection.find())
    
    def get_by_session(self,session_id):
        return list(self.collection.find({"session_id":session_id}))