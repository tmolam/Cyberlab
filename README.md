# Cyberlab

This is a containerized  cybersecurity lab built with Docker Compose for my own learning purposes.

This includes application security, network segmentation, centralized logging and detection.

## WARNING!

This project intentionally contains vulnerable applications and is designed for learning.
Run only in an isolated environment.

## Architecture

attacker01 -> web01 (Nginx) -> app01 (Flask) -> db01 (MariaDB)

app01 -> Alloy -> Loki -> Grafana

## Technologies

Docker Compose

Nginx

Python / Flask

MariaDB

Grafana Alloy

Grafana Loki

Grafana

## Security Exercises

SQL injection

Authentication bypass

Brute-force detection

Network segmentation

Logging

Alerting

## Status

This is an ongoing personal cybersecurity learning project
