import os
import subprocess
from datetime import datetime
import google.generativeai as genai
import logging
import sys
import ast

# Configure logging for detailed debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API with your key
GEMINI_API_KEY = "AIzaSyD2aTpevz81EFI4LFwQjq_ELeHnGg1ruJ8"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# Scene System Prompt for generating structured outlines
SCENE_SYSTEM_PROMPT = """
Generate a structured outline for a given topic with the following sections:
- Topic: The main subject to explain.
- Key Points: 3-5 core concepts or steps to cover.
- Visual Elements: Specific Manim objects (e.g., shapes, text, graphs) to represent each key point.
- Style: Use a 3Blue1Brown-inspired style with smooth animations, consistent colors (e.g., BLUE, GREEN, WHITE), and clear transitions.
For computer science/math topics (e.g., arrays, linked lists, binary search), include data structure visualizations and time complexity (e.g., O(n), O(log n)) with graphs or annotations.
"""

# Updated Manim System Prompt with detailed instructions
MANIM_SYSTEM_PROMPT = """
You are an expert in creating educational animations using Manim (version 0.18.1). Your task is to generate a Python script for a Manim animation that visually explains a given topic based on a structured outline. The code must be original, syntactically correct, adhere to Manim's requirements, and compile successfully to produce a video. Follow these steps:

### 1. Understand the Outline
- Use the provided structured outline (Topic, Key Points, Visual Elements, Style) to plan the animation.
- Identify core concepts and their visual representations.

### 2. Plan the Animation
- Create a logical sequence of animations that follows the outline’s key points.
- Use visual elements (e.g., shapes, text, graphs) within screen bounds (-7.5 to 7.5 x-axis, -4 to 4 y-axis).
- Ensure no overlapping objects and smooth scene transitions.

### 3. Write the Manim Code
- **Imports**: Start with `from manim import *`.
- **Class**: Define a single class named `Scene` inheriting from `Scene`.
- **Construct Method**: Implement the `construct` method with animations for each key point.
- **Modularity**: Use helper methods (e.g., `create_array`, `create_graph`) for clarity.
- **Comments**: Add clear comments for each section.
- **Transitions**: Use `self.play(FadeOut(*self.mobjects))` to clear scenes, but only after mobjects are added.
- **Pacing**: Add `self.wait(1)` after key animations for readability.
- **Style**: Apply a 3Blue1Brown style with colors like BLUE, GREEN, WHITE and smooth effects.

### 4. Ensure Code Correctness
- Verify syntax (close all parentheses, brackets, braces).
- Define all variables before use.
- Use only Manim 0.18.1 methods (e.g., `Circle`, `Text`, `Create`, `FadeOut`).
- Avoid errors like fading out an empty scene at the start of `construct`.

### 5. Topic-Specific Requirements
- For computer science topics (e.g., arrays, linked lists, binary search):
  - Visualize data structures (e.g., boxes for arrays, nodes with arrows for linked lists).
  - Animate algorithms step-by-step (e.g., binary search splitting an array).
  - Show time complexity (e.g., O(n), O(log n)) with text or graphs.
- For math topics (e.g., Pythagorean theorem):
  - Use geometric shapes (e.g., triangles, squares) and equations (e.g., \(a^2 + b^2 = c^2\)).
  - Animate transformations or proofs.

### 6. Output the Code
- Provide a complete script ready to run with `manim -qm script.py Scene -o output.mp4`.
- Enclose the code in ```python``` markers.
"""

def generate_outline(topic):
    """Generate a structured outline for the given topic using Gemini API."""
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"{SCENE_SYSTEM_PROMPT}\n\nGenerate a structured outline for the topic: '{topic}'"
    try:
        response = model.generate_content(prompt)
        outline = response.text.strip()
        logger.info("Successfully generated outline")
        return outline
    except Exception as e:
        logger.error(f"Outline generation error: {str(e)}")
        raise Exception(f"Outline generation error: {str(e)}")

def generate_manim_code(outline, topic, error_feedback=None):
    """Generate Manim code based on the outline, with optional error feedback for correction."""
    model = genai.GenerativeModel('gemini-pro')
    prompt = (
        f"{MANIM_SYSTEM_PROMPT}\n\n"
        f"Generate an original Manim Python script to visually explain '{topic}' based on this outline:\n{outline}"
    )
    if error_feedback:
        prompt += (
            f"\n\nPrevious Error Feedback: The last attempt failed with:\n{error_feedback}\n"
            "Revise the code to fix this issue and ensure it compiles successfully."
        )
    try:
        response = model.generate_content(prompt)
        manim_code = response.text.strip()
        if manim_code.startswith("python") and manim_code.endswith("```"):
            manim_code = manim_code[9:-3].strip()
        logger.info("Successfully generated Manim code")
        return manim_code
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        raise Exception(f"Gemini API error: {str(e)}")

def validate_code(code):
    """Validate the syntax of the generated code using Python's AST module."""
    try:
        ast.parse(code)
        logger.info("Code syntax is valid")
        return True
    except SyntaxError as e:
        logger.error(f"Syntax error in generated code: {e}")
        return f"SyntaxError: {str(e)}"

def compile_manim_code(script_path, video_path):
    """Compile the Manim script into a video."""
    result = subprocess.run(
        [sys.executable, "-m", "manim", "-qm", script_path, "Scene", "-o", video_path],
        capture_output=True,
        text=True
    )
    logger.info(f"Manim stdout: {result.stdout}")
    if result.stderr:
        logger.error(f"Manim stderr: {result.stderr}")
    return result

def generate_manim_code_and_video(topic):
    """Generate Manim code and compile it into a video, self-correcting errors."""
    logs = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "output_videos"
    os.makedirs(output_dir, exist_ok=True)

    logs.append(f"Generating outline for topic: {topic}")
    try:
        outline = generate_outline(topic)
        logs.append(f"Outline generated:\n{outline}")
    except Exception as e:
        logs.append(f"Failed to generate outline: {str(e)}")
        raise

    attempt = 1
    error_feedback = None
    max_attempts = 5  # Limit to prevent infinite loops

    while attempt <= max_attempts:
        logs.append(f"Attempt {attempt}: Generating Manim code")
        try:
            manim_code = generate_manim_code(outline, topic, error_feedback)
            logs.append(f"Generated code:\n{manim_code}")

            # Validate syntax
            syntax_result = validate_code(manim_code)
            if syntax_result is not True:
                error_feedback = syntax_result
                logs.append(f"Syntax validation failed: {error_feedback}")
                attempt += 1
                continue

            # Save code to a file in output_dir
            script_path = os.path.join(output_dir, f"script_{timestamp}_attempt{attempt}.py")
            video_path = os.path.join(output_dir, f"video_{timestamp}_attempt{attempt}.mp4")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(manim_code)
            logs.append(f"Manim code saved to {script_path}")

            # Compile with Manim
            logs.append("Starting Manim compilation...")
            result = compile_manim_code(script_path, video_path)
            logs.append(f"Manim output: {result.stdout}")
            if result.stderr:
                logs.append(f"Manim errors: {result.stderr}")

            # Check if compilation was successful and video exists
            if result.returncode == 0 and os.path.exists(video_path):
                logs.append("Compilation successful!")

                # Clean up temporary script file
                if os.path.exists(script_path):
                    os.remove(script_path)
                return {"video_path": video_path, "logs": logs}
            else:
                error_lines = result.stderr.splitlines()
                if any("ValueError: At least one mobject must be passed" in line for line in error_lines):
                    error_feedback = (
                        "Error: Attempted to fade out mobjects when the scene was empty at the start. "
                        "Remove initial FadeOut calls."
                    )
                elif any("FileNotFoundError" in line for line in error_lines):
                    error_feedback = "Error: Manim could not find the output directory or file path."
                else:
                    error_feedback = (
                        f"Manim compilation failed with exit code {result.returncode}\n"
                        f"Errors:\n{result.stderr}"
                    )
                logs.append(f"Compilation failed: {error_feedback}")
                attempt += 1

        except Exception as e:
            logs.append(f"Error in attempt {attempt}: {str(e)}")
            error_feedback = str(e)
            attempt += 1

    logs.append(f"Max attempts ({max_attempts}) reached. Video generation failed.")
    raise Exception(f"Failed to generate video after {max_attempts} attempts.")