<div align="center">

# 💰 Finance Bot

### Turn a bank statement PDF into a clear spending dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Aiven-4479A1?logo=mysql&logoColor=white)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render&logoColor=white)

**[🔗 Live Demo](https://finance-analizer.onrender.com)**

</div>

---

## Overview

Upload a bank statement PDF and get an instant breakdown of your spending — automatically categorized, with charts and downloadable reports.

> ⚠️ Hosted on Render's free tier — first request after inactivity can take 30–60 seconds to wake up.

## Features

- 📄 Extracts transactions and account details directly from a bank statement PDF
- 🏷️ Categorizes each transaction using 500+ keyword rules + fuzzy matching for unknown merchants
- 🤝 Separates person-to-person transfers from real merchant spending
- 📊 Web dashboard with spending summary, category breakdown, and charts
- 📑 Downloadable Excel and PDF reports
- ☁️ Every statement is saved to a cloud MySQL database

## Tech Stack

Python · FastAPI · HTML/CSS/JS · MySQL (Aiven) · pandas · pdfplumber · reportlab · matplotlib · rapidfuzz · Render

## How Categorization Works

1. Checks the merchant name against 500+ known keywords
2. Falls back to fuzzy matching for anything not in the list
3. "Payment from/for" patterns without a merchant match → labeled Person Transfer
4. Anything left over → Uncategorized
