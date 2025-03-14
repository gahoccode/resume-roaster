---
title: Resume Roaster
emoji: ⚡
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 5.15.0
app_file: main.py
pinned: false
tags:
- smolagents
- agent
- smolagent
- tool
- agent-course
---

# Resume Roaster

A fun application that "roasts" your resume in a humorous but professional way.

## Credits

This project was originally created by [Kuber Mehta](https://github.com/Kuberwastaken) and is hosted on Hugging Face Spaces:
[https://huggingface.co/spaces/Kuberwastaken/resume-roaster](https://huggingface.co/spaces/Kuberwastaken/resume-roaster)

This repository is a fork with additional Docker configuration and local model support.

## Setup and Running Locally

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your environment:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file to configure your preferred model:
   - For OpenAI: Set `MODEL_TYPE=openai` and add your `OPENAI_API_KEY`
   - For Ollama: Set `MODEL_TYPE=ollama` and ensure Ollama is running locally

4. Run the application:
   ```
   python main.py
   ```

5. Open the Gradio interface in your browser and upload a resume PDF or paste resume text.

## Docker Deployment

### Using Docker Compose (Recommended)

1. Set up your environment:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file to configure your preferred model:
   - For OpenAI: Set `MODEL_TYPE=openai` and add your `OPENAI_API_KEY`
   - For Ollama: Set `MODEL_TYPE=ollama` (see Ollama integration below)

3. Build and start the containers:
   ```
   docker-compose up -d
   ```

4. Access the application at http://localhost:7860

5. To stop the application:
   ```
   docker-compose down
   ```

### Using Ollama with Docker

To use Ollama within Docker:

1. Uncomment the Ollama service in `docker-compose.yml`
2. Set `MODEL_TYPE=ollama` and `OLLAMA_URL=http://ollama:11434` in your `.env` file
3. Run `docker-compose up -d`
4. The first run will download the Ollama model, which may take some time

### Using Docker Manually

1. Build the Docker image:
   ```
   docker build -t resume-roaster .
   ```

2. Run the container:
   ```
   docker run -p 7860:7860 --env-file .env resume-roaster
   ```

3. Access the application at http://localhost:7860

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
