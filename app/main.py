from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .database.connection import initialize_databases

# Create FastAPI app
app = FastAPI(
    title="Student Performance API",
    description="API for managing student performance data and predictions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")

# Initialize event handlers
@app.on_event("startup")
async def startup_event():
    """Initialize databases on startup"""
    initialize_databases()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Student Performance API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


