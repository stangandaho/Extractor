from qgis.core import QgsTask, QgsApplication, Qgis
from qgis.PyQt.QtWidgets import QApplication

class TaskManager(QgsTask):
    def __init__(self, description, total_steps, owner):
        super().__init__(description, QgsTask.CanCancel, owner)
        self.total_steps = total_steps
        self.current_step = 0

    def run(self):
        # Your task code here
        for i in range(self.total_steps):
            # Update progress
            self.current_step += 1
            progress = int(100 * self.current_step / self.total_steps)
            self.setProgress(progress)

            # Check for cancellation
            if self.isCanceled():
                return False

            # Process application events to allow GUI to update
            QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

        return True
