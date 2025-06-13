import asyncio


class MonitoringManager:
    def __init__(self):
        self.tasks = {}

    def add_task(self, user_id: int, article: str, task: asyncio.Task):
        key = (user_id, article)
        self.tasks[key] = task

    def cancel_task(self, user_id: int, article: str):
        key = (user_id, article)
        task = self.tasks.pop(key, None)
        if task:
            task.cancel()

    def get_user_articles(self, user_id: int):
        return [article for (uid, article) in self.tasks if uid == user_id]


monitoring_manager = MonitoringManager()
