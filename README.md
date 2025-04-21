# 🔐 Certificate Checker

This python script will check the duration left of a domain's TLS certificate. It will send an email if the expiry date is less than the threshold days. This script is useful for interfaces that do not allow for automatic renewal of TLS certs by providing an email reminder.

---

## 🚀 Features

- 🔁 Runs Automatically – Can be scheduled with Task Scheduler/Cron job.
- 📧 Email Alerts – Sends an email if certificate duration is less than specified duration.
- 🛠 Error Notifications – Emails you if the script fails.

---

## 🛠 Installation & Setup

### 1️⃣ Prerequisites

- Python 3.x
- Proton Mail+ Account

Special Note: Emails
You can use another method of sending emails if you do not have a Proton Mail+ account, as the Proton Mail Bridge is only available to ProtonMail+ users

### 2️⃣ Configure Environment Variables

Set the following environment variables:

``` bash
website_url = "your_website_url"
protonmail_email_address = "your_email_address"
protonmail_bridge_pass = "your_protonmail_bridge_password"

```

### 3️⃣ Automate with Task Scheduler/Cron Jobs

Task Scheduler

1. Open Task Scheduler (taskschd.msc).
2. Create a new task.
3. Set trigger: Every X days/weeks.
4. Set action: Run Python with the script.

Cron Job

1. Run ```crontab -e```
2. Add ```0 0 */2 * * /usr/bin/python3 /path/to/script.py```
3. Replace ```/path/to/script.py``` with the actual path to your script
4. Adjust when and how often you would like the script to run (command in 2. runs every 2 days at mightnight(00:00))

Note: check documentation for help on how to use cron jobs

---

## 📜 Example Output

✅ TLS cert expiry date > 30 days:

``` bash
No email is sent to reduce clutter in inbox
```

🚨 TLS cert expiry date < 30 days:

``` bash
Certificate for example.com expires on 20/07/2025 14:40:00 (89 days left)
```

---

## 📌 How It Works

1. Make connection to domain
2. Get TLS certificate
3. Extract expiry date ("Not After" field)
4. Compare expiry date to threshold days
    - if less than threshold days
        - sends email
    - if more than threshold days
        - does not send email

---

## 📝 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it, but please provide attribution by keeping my name in the copyright notice.

If you improve the script or use it in a project, a shoutout or a mention would be appreciated! 😊

---

## 📋 Notes

You can change the date format if you wish.
