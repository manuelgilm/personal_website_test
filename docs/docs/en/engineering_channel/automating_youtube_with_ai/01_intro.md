# What are we building?

Welcome to **Automating YouTube with AI**, a series where we build a production-grade autonomous agent that monitors a YouTube channel and replies to comments — powered by Go, MLflow, OpenAI, and GitHub Actions.

## The problem

As a YouTube creator grows, the comment section becomes harder to keep up with. Most questions ask about things already covered in the video, yet answering them takes time and breaks creative flow. Ignoring them hurts engagement and the algorithm.

## The solution: tubectl

**tubectl** is a Go CLI tool that connects to the YouTube Data API v3 and automates the entire reply workflow:

1. A GitHub Actions workflow runs every hour (cron)
2. Reads a YAML config of video IDs to monitor
3. Fetches new comments since the last run
4. Checks a local cache to avoid re-replying
5. Retrieves the video transcript via YouTube Captions API
6. Sends the transcript + comment to OpenAI with a system prompt
7. Posts the generated reply back to YouTube
8. Updates the cache for the next cycle

All logic lives in the `tubectl` binary — the workflow is just the scheduler.

## The role of MLflow

The bot's intelligence comes from its system prompt. We use MLflow to treat prompt engineering as a proper ML workflow:

- Define candidate prompts (zero-shot, few-shot, role, role+CoT)
- Run them against a synthetic Q&A dataset
- Track metrics, parameters, and traces in MLflow
- Compare experiments and promote a **champion prompt** to production

## Series overview

| Video | Title | What you will learn |
|-------|-------|-------------------|
| 1 | **The Blueprint** | Full architecture walkthrough, dataset creation, evaluation framework |
| 2 | **The Prompt Showdown** | 4 prompting techniques, MLflow experiment tracking, champion selection |
| 3 | **tubectl: The YouTube Connector** | CLI structure, comments, transcripts, the `bot answer-comment` command |
| 4 | **The Inference Pipeline** | Runtime journey: trigger → cache → transcript → LLM → post |
| 5 | **Production: From Cron to Live** | GitHub Actions, secrets, live demo, monitoring |

## Prerequisites

- Basic knowledge of Python and the command line
- A Google Cloud Platform project with the YouTube Data API v3 enabled
- An OpenAI API key
- A GitHub repository
- MLflow installed (local or remote tracking server)

Let's build something real.
