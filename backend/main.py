from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import logging
from manim_runner import generate_manim_code_and_video

# Configure logging for detailed debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Define the request model for the /generate-video endpoint
class TopicRequest(BaseModel):
    topic: str

@app.post("/generate-video")
async def generate_video(request: TopicRequest):
    """
    Endpoint to generate a Manim video based on a topic.
    Expects a JSON body with a 'topic' field (e.g., {"topic": "@visual binary search"}).
    Returns the video URL and logs upon success.
    """
    try:
        logger.info(f"Received request with topic: {request.topic}")
        # Extract the topic by removing "@visual " prefix
        topic = request.topic.replace("@visual ", "").strip()
        logger.info(f"Processed topic: {topic}")

        # Generate Manim code and compile it into a video
        output_data = generate_manim_code_and_video(topic)
        video_path = output_data["video_path"]
        logs = output_data["logs"]

        # Verify the video file exists
        if not os.path.exists(video_path):
            logger.error(f"Video file not found at {video_path}")
            raise HTTPException(status_code=500, detail="Video generation failed: File not created")

        logger.info(f"Video generated successfully at {video_path}")
        return {
            "video_url": f"/videos/{os.path.basename(video_path)}",
            "logs": logs,
            "message": "Video generated successfully"
        }
    except Exception as e:
        logger.exception(f"Error in generate_video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

@app.get("/videos/{filename}")
async def get_video(filename: str):
    """
    Endpoint to serve the generated video file.
    Takes a filename and returns the video if it exists.
    """
    video_path = os.path.join("output_videos", filename)
    if os.path.exists(video_path):
        logger.info(f"Serving video: {video_path}")
        return FileResponse(video_path, media_type="video/mp4")
    logger.error(f"Video not found: {video_path}")
    raise HTTPException(status_code=404, detail="Video not found")

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI server on localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)