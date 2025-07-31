from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from endpoints.users import router as users_router
from endpoints.auth import router as auth_router
from endpoints.sessions import router as sessions_router
from endpoints.courses import router as courses_router
from endpoints.lessons import router as lessons_router
from endpoints.assignments import router as assignments_router
from endpoints.grades import router as grades_router
from endpoints.progress import router as progress_router
from endpoints.notifications import router as notifications_router
from endpoints.files import router as files_router
from endpoints.analytics import router as analytics_router
from endpoints.reports import router as reports_router
from endpoints.settings import router as settings_router
from endpoints.calendar import router as calendar_router
from endpoints.messages import router as messages_router
from endpoints.payments import router as payments_router
from endpoints.subscriptions import router as subscriptions_router
from endpoints.feedback import router as feedback_router
from endpoints.support import router as support_router
from endpoints.admin import router as admin_router
from endpoints.learning_sessions import router as learning_sessions_router
from endpoints.ai_tutor import router as ai_tutor_router
from endpoints.families import router as families_router
from endpoints.device_monitoring import router as device_monitoring_router
from endpoints.parental_controls import router as parental_controls_router
from endpoints.anti_cheat import router as anti_cheat_router
from endpoints.gamification import router as gamification_router
from endpoints.content import router as content_router
from endpoints.assessments import router as assessments_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assessments_router)
app.include_router(content_router)
app.include_router(gamification_router)
app.include_router(anti_cheat_router)
app.include_router(parental_controls_router)
app.include_router(device_monitoring_router)
app.include_router(families_router)
app.include_router(ai_tutor_router)
app.include_router(learning_sessions_router)
app.include_router(admin_router)
app.include_router(support_router)
app.include_router(feedback_router)
app.include_router(subscriptions_router)
app.include_router(payments_router)
app.include_router(messages_router)
app.include_router(calendar_router)
app.include_router(settings_router)
app.include_router(reports_router)
app.include_router(analytics_router)
app.include_router(files_router)
app.include_router(notifications_router)
app.include_router(progress_router)
app.include_router(grades_router)
app.include_router(assignments_router)
app.include_router(lessons_router)
app.include_router(courses_router)
app.include_router(sessions_router)
app.include_router(auth_router)
app.include_router(users_router)
@app.get("/api/status")
async def get_status():
    return {"status": "operational", "version": "1.0.0"}

@app.get("/api/data")
async def get_data():
    # TODO: Implement data endpoint
    return {"data": []}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)