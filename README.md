# Forex Update Notifier

A small personal automation project that tracks the GBP exchange rate published by **Nepal Rastra Bank (NRB)** and sends a push notification whenever it runs — so I don't have to manually check the rate every day.

---

## What It Does

The pipeline runs end-to-end in four steps:

1. **Fetch** — Pulls the latest currency exchange data from the NRB API.
2. **Parse** — Extracts the GBP rate from the raw response.
3. **Store** — Appends the record to a local CSV file so historical rates are logged over time.
4. **Notify** — Sends a push notification to my phone via [ntfy](https://ntfy.sh/) with the current rate.

If any step fails, the error is logged so it's easy to see what went wrong.

---

## Why I Built This

I wanted a lightweight, zero-cost way to keep an eye on the GBP/NPR exchange rate without opening a banking site or app every day. Instead of building a full dashboard, this project just does the one thing I actually needed: fetch the rate and ping my phone.

---

## Tech Stack

- **Python** — core scripting and orchestration
- **NRB API** — source of official exchange rate data
- **ntfy** — free push notification service
- **GitHub Actions** — runs the pipeline on a schedule, no server required

---

## Running It Yourself

1. Clone the repo:
   ```bash
   git clone https://github.com/SiddhantR0/Forex-Update-Notifier.git
   cd Forex-Update-Notifier
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the pipeline:
   ```bash
   python main.py
   ```

By default, it tracks the GBP rate and pushes notifications to a specific ntfy topic — update the topic name in `main.py` if you want to use your own.

---

## Status

This is a personal side project built for my own daily use.