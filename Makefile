# Makefile for Spotify Listening History Project

# Load .env if needed
include .env
export

# Variables
COMPOSE=docker-compose
AIRFLOW_IMAGE=apache/airflow:2.9.1

.PHONY: help build up down restart logs init-airflow bash-webserver

help:
	@echo "Makefile commands:"
	@echo "  build           Build all services"
	@echo "  up              Start all containers"
	@echo "  down            Stop and remove containers"
	@echo "  restart         Restart all services"
	@echo "  logs            Show logs for all containers"
	@echo "  init-airflow    Initialize Airflow DB and admin user"
	@echo "  bash-webserver  Open shell in Airflow webserver"
	@echo "  airflow-ui      Open Airflow UI in browser"

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart: down up

logs:
	$(COMPOSE) logs -f

init-airflow:
	@echo "Initializing Airflow DB and creating admin user..."
	$(COMPOSE) run --rm airflow-init

bash-webserver:
	$(COMPOSE) exec airflow-webserver /bin/bash

airflow-ui:
	open http://localhost:8080
