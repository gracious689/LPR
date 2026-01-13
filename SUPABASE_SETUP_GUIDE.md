# Supabase Database Setup Guide

## Step 1: Create Supabase Project
1. Go to https://supabase.com
2. Click "Start your project" 
3. Sign up/login
4. Create new organization (if needed)
5. Create new project:
   - Choose a name (e.g., "lpr-system")
   - Choose a database password
   - Select a region closest to you
   - Click "Create new project"

## Step 2: Get Your Credentials
1. Wait for project to be ready (2-3 minutes)
2. Go to your project dashboard
3. Click on **Settings** (gear icon)
4. Select **API** from the sidebar
5. You'll see:
   - **Project URL** (something like: https://xxxxxxxx.supabase.co)
   - **anon public** key (starts with: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...)

## Step 3: Update .env File
Replace the placeholders in your `.env` file:

```env
# Supabase Configuration
SUPABASE_URL=https://your-actual-project-id.supabase.co
SUPABASE_KEY=your-actual-anon-key-here

# Tesseract Path (Windows)
TESSERACT_PATH=C:\Users\hp\Downloads\5.5.2 source code\tesseract-ocr-tesseract-9c516f4\tesseract.exe
```

## Step 4: Create Database Table
1. In your Supabase project, click on **SQL Editor** in the sidebar
2. Click "New query"
3. Copy the contents of `SUPABASE_SQL.sql`
4. Paste it into the SQL editor
5. Click **Run** to execute the SQL

## Step 5: Verify Setup
1. Go to **Table Editor** in the sidebar
2. You should see the `license_plates` table
3. Click on it to verify the structure

## Step 6: Test Connection
After updating your `.env` file with real credentials, run:
```bash
python test_system.py
```

You should see:
- ✅ Supabase connection is working

## Step 7: Initialize System
```bash
python main.py --mode setup
```

## Troubleshooting

### "Invalid URL" error:
- Make sure your URL starts with `https://`
- Don't include trailing slash
- Example: `https://abcdefgh.supabase.co`

### "Invalid API key" error:
- Copy the entire "anon public" key
- Make sure there are no extra spaces
- Key should start with `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### Table not found:
- Make sure you ran the SQL in Step 4
- Check that the table name is exactly `license_plates`
