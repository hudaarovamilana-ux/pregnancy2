# Deploy to Vercel (Telegram Webhook)

## 1) Push project to GitHub

Vercel deploys from a Git repository.

## 2) Create Vercel project

- Import repository into Vercel
- Framework preset: **Other**
- Root directory: project root

## 3) Add environment variables in Vercel

- `BOT_TOKEN` - Telegram bot token
- `WEBHOOK_SECRET` - random secret string (recommended)

Optional:

- `DATABASE_PATH` - custom SQLite path (by default Vercel uses `/tmp/pregnancy_bot.db`)

## 4) Deploy

After deploy, your public URL is usually:

`https://<project>.vercel.app`

## 5) Set Telegram webhook

Run locally once:

```bash
set BOT_TOKEN=your_token
set VERCEL_URL=https://<project>.vercel.app
set WEBHOOK_SECRET=your_secret
python setup_webhook_vercel.py
```

PowerShell variant:

```powershell
$env:BOT_TOKEN="your_token"
$env:VERCEL_URL="https://<project>.vercel.app"
$env:WEBHOOK_SECRET="your_secret"
python setup_webhook_vercel.py
```

## 6) Test

- Send `/start` in Telegram
- Check Vercel function logs if needed

## Important note about SQLite on Vercel

Vercel serverless filesystem is ephemeral. SQLite in `/tmp` can reset between cold starts.
For production persistent storage, migrate to external DB (PostgreSQL, Supabase, Neon, etc.).
