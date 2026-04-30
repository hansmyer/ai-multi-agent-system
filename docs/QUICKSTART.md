"""
Quick Start Guide for AI Multi-Agent System
"""

# Quick Start Guide

## 1. Installation

### Option A: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/hansmyer/ai-multi-agent-system.git
cd ai-multi-agent-system

# Setup environment
cp .env.example .env

# Add your credentials
# Edit .env and set:
# OPENAI_API_KEY=your_key_here
# GITHUB_TOKEN=your_token_here

# Start system
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f
