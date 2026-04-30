# Makefile for AI Multi-Agent System

.PHONY: help setup install run docker-build docker-up docker-down logs test lint format clean

help:
	@echo "AI Multi-Agent System - Available Commands"
	@echo "==========================================="
	@echo "make setup          - Setup development environment"
	@echo "make install        - Install dependencies"
	@echo "make run            - Run locally"
	@echo "make docker-build   - Build Docker image"
	@echo "make docker-up      - Start Docker containers"
	@echo "make docker-down    - Stop Docker containers"
	@echo "make logs           - View Docker logs"
	@echo "make test           - Run tests"
	@echo "make lint           - Run linting"
	@echo "make format         - Format code"
	@echo "make clean          - Clean up"

setup:
	@echo "Setting up development environment..."
	python -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

run:
	@echo "Starting AI Multi-Agent System..."
	python -m src.main

docker-build:
	@echo "Building Docker image..."
	docker-compose -f docker/docker-compose.yml build

docker-up:
	@echo "Starting Docker containers..."
	docker-compose -f docker/docker-compose.yml up -d
	@echo "Containers started. View logs with: make logs"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose -f docker/docker-compose.yml down

logs:
	@echo "Showing Docker logs..."
	docker-compose -f docker/docker-compose.yml logs -f ai-agent-system

test:
	@echo "Running tests..."
	pytest tests/ -v --cov=src

lint:
	@echo "Running linting..."
	flake8 src/ --max-line-length=100
	mypy src/ --ignore-missing-imports

format:
	@echo "Formatting code..."
	black src/ tests/ examples/
	isort src/ tests/ examples/

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage
	rm -rf build dist *.egg-info
