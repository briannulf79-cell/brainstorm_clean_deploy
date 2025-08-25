# 🌐 **VERCEL FRONTEND ENVIRONMENT VARIABLE FIX**

## 🚨 **CRITICAL ISSUE IDENTIFIED:**

Your frontend is trying to connect to `localhost:5000` instead of your Railway backend URL.

The console errors show:
```
❌ localhost:5000/api/auth/login - Failed to load resource: net::ERR_CONNECTION_REFUSED
❌ localhost:5000/api/auth/demo - Failed to load resource: net::ERR_CONNECTION_REFUSED
❌ localhost:5000/api/auth/signup - Failed to load resource: net::ERR_CONNECTION_REFUSED
```

---

## 🔧 **FIX REQUIRED:**

### **Step 1: Get Your Railway Backend URL**
1. Go to your Railway project dashboard
2. Copy the URL from the "Domains" section (something like: `https://brainstorm-clean-deploy-production.up.railway.app`)

### **Step 2: Update Vercel Environment Variable**
1. Go to your Vercel project dashboard
2. Go to **Settings** → **Environment Variables**
3. Find `VITE_API_URL` (or add it if missing)
4. Set value to: `https://your-railway-backend-url.railway.app`
5. **IMPORTANT:** Remove any trailing slash

### **Step 3: Redeploy Vercel**
1. Go to **Deployments** tab
2. Click **"Redeploy"** on the latest deployment
3. Or push a new commit to trigger auto-deploy

---

## ✅ **EXPECTED RESULT:**

After fixing the environment variable:
- ✅ Login will work
- ✅ Demo access will work  
- ✅ Registration will work
- ✅ All API calls will reach your Railway backend

---

## 🎯 **EXAMPLE:**

If your Railway URL is: `https://web-production-abc123.up.railway.app`

Then in Vercel set:
```
VITE_API_URL=https://web-production-abc123.up.railway.app
```

**No trailing slash!**

---

## 🔍 **HOW TO VERIFY:**

After redeploying Vercel:
1. Open browser developer tools (F12)
2. Go to Network tab
3. Try to login/register
4. You should see API calls going to your Railway URL instead of localhost:5000

---

**This is the main issue preventing login/demo access!** 🚨