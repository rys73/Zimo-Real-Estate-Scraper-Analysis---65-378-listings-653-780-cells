# Real Estate Web Scraping & Data Analysis Project
**Project: Zimo Real Estate Market Analysis**
---

## Overview
This is a **personal and educational project** aimed at learning and demonstrating web scraping, data cleaning, and data analysis skills.
The project consists of a full pipeline to scrape French real estate listings, process the data, and generate detailed insights.
- **Total entries scraped:** 65,378 rows
- **Columns per listing:** 10
- **Total data points:** 653,780

It is designed purely for **educational purposes** and personal skill development.
---

## Features

### Web Scraping
- Scrapes property listings from [Zimo.fr](https://www.zimo.fr) using **Playwright**.
- Extracts:
- City
- Property type (Maison/Apartment)
- Title
- Price
- Price per square meter
- Surface area
- Professional or private seller
- Listing date
- URL
- Description
- Handles dynamic content, cookies, and pagination.
- Saves CSV files per city/type and a global CSV.

### Data Cleaning & Processing
- Cleans price and surface area for numeric analysis.
- Converts relative dates (e.g., "Il y a 3 jours") into absolute timestamps.
- Handles missing or inconsistent data.

### Data Analysis & Visualization
- Generates **global PDF reports**:
- Average and median price per city
- Price by property type
- Price by surface ranges
- Professional vs private sellers
- Scatter plots and histograms
- Generates **per-city PDF reports**:
- Mean/median price
- Price deviation from median
- Top 10 opportunities
- Average price per property type
- Surface analysis
- Listing age analysis
- Summary “mental map” of each city’s market
- Uses **Pandas**, **Matplotlib**, and **Seaborn** for all analysis.
---
