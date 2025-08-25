# 🔑 API Keys Setup Guide - FIXED DEPLOYMENT READY

## 🚨 **DEPLOYMENT ISSUES FIXED!**

I've identified and fixed the Railway deployment issues:

✅ **Fixed Requirements** - Updated dependencies and versions  
✅ **Added Gunicorn** - Production WSGI server for Railway  
✅ **Created WSGI Entry** - Proper Flask app entry point  
✅ **Updated Procfile** - Railway deployment configuration  
✅ **Error Handling** - Graceful service import fallbacks  

---

## 🔧 **STEP 1: GET YOUR API KEYS**

### 📧 **Mailgun (Email Service)**
1. Go to: **https://app.mailgun.com**
2. Sign up for free account (10,000 emails/month)
3. Get your API key from: Settings → API Keys
4. Get your domain from: Sending → Domains

### 💳 **Stripe (Payments)**  
1. Go to: **https://dashboard.stripe.com**
2. Sign up for account
3. Get Secret Key from: Developers → API Keys
4. Create webhook endpoint for: `https://your-app.railway.app/api/stripe/webhook`
5. Get webhook secret from webhook settings

### 📱 **Twilio (SMS)**
1. Go to: **https://console.twilio.com**  
2. Sign up for account ($20 free credit)
3. Get Account SID and Auth Token from dashboard
4. Buy phone number from: Phone Numbers → Manage

### 🤖 **OpenAI (AI Features)**
1. Go to: **https://platform.openai.com**
2. Create account and add payment method
3. Get API key from: API Keys section

---

## 🚀 **STEP 2: DEPLOY TO RAILWAY**

### **Connect Repository:**
1. Go to **railway.app**
2. Click "New Project" → "Deploy from GitHub repo"  
3. Select: `brainstorm_clean_deploy`
4. Set root directory: `backend`

### **Add Environment Variables:**
Click your Railway project → Variables tab → Add these:

```
JWT_SECRET_KEY=your-super-secret-jwt-key-make-it-very-long
FLASK_ENV=production
FLASK_DEBUG=False
MAILGUN_API_KEY=your_mailgun_api_key_here
MAILGUN_DOMAIN=your_mailgun_domain_here  
FROM_EMAIL=noreply@brainstormaikit.com
STRIPE_SECRET_KEY=your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here
OPENAI_API_KEY=your_openai_api_key_here
FRONTEND_URL=https://your-vercel-app.vercel.app
```

**Railway will automatically:**
- Provide PostgreSQL database (DATABASE_URL)
- Install dependencies from requirements.txt
- Start app using Procfile with gunicorn

---

## 🌐 **STEP 3: DEPLOY FRONTEND TO VERCEL**

1. Go to **vercel.com**
2. Click "New Project" → Import your repository
3. Set root directory: `frontend`
4. Add environment variable:
   ```
   VITE_API_URL=https://your-railway-backend.railway.app
   ```

---

## ✅ **STEP 4: TEST YOUR DEPLOYMENT**

### **Test Backend Health:**
Visit: `https://your-railway-app.railway.app/api/health`  
Should return: `{"status": "healthy"}`

### **Test User Registration:**
1. Go to your frontend URL
2. Try registering a new account
3. Check you receive welcome email
4. Verify account creation works

### **Test Admin Features (Master Account):**
1. Login with: `brian.nulf79@gmail.com`
2. Go to: `/api/admin/service-status`
3. Verify all services show as enabled

---

## 🔍 **TROUBLESHOOTING**

### **Railway Build Fails:**
- Check Railway deployment logs
- Verify all dependencies in requirements.txt
- Ensure Python version compatibility

### **App Won't Start:**
- Check Railway runtime logs  
- Verify wsgi.py exists and is correct
- Ensure Procfile uses gunicorn correctly

### **Service Errors:**
- Check environment variables are set correctly
- Verify API keys are valid and active
- Test individual service endpoints

### **Database Issues:**
- Railway auto-provides DATABASE_URL
- Check database connection in logs
- Verify PostgreSQL URL format

---

## 🎯 **WHAT'S BEEN FIXED**

### **Before (Issues):**
❌ Wrong Python dependencies  
❌ Missing production WSGI server  
❌ Incorrect Procfile configuration  
❌ No graceful error handling  
❌ Service import failures  

### **After (Fixed):**
✅ Clean, production-ready requirements.txt  
✅ Gunicorn WSGI server for Railway  
✅ Proper wsgi.py entry point  
✅ Updated Procfile for production  
✅ Graceful service import fallbacks  
✅ Ready for Railway deployment  

---

## 📞 **NEED HELP?**

### **Railway Deployment Issues:**
1. Check "Deployments" tab in Railway dashboard
2. View build and runtime logs
3. Verify environment variables are set

### **Service Integration Issues:**
1. Use `/api/admin/service-status` endpoint
2. Check individual service configurations
3. Verify API keys are correctly formatted

### **Frontend Connection Issues:**
1. Check CORS configuration
2. Verify VITE_API_URL points to Railway backend
3. Test API endpoints directly

---

## 🎉 **SUCCESS!**

Once deployed, your Brainstorm AI Kit will have:

✅ **Automated Email System** - Welcome emails, trial warnings, password resets  
✅ **SMS Notifications** - Multi-channel communication  
✅ **Payment Processing** - Stripe subscription management  
✅ **AI Features** - Lead scoring, content generation  
✅ **Trial Management** - 30-day trials with automated conversion  
✅ **Admin Tools** - Master account with full control  

**Your platform is now ready to compete with Go High Level!** 🚀

---

## 📥 **DOWNLOAD ALL PROJECT FILES**

**GitHub Repository:** https://github.com/briannulf79-cell/brainstorm_clean_deploy

**To Download Everything:**
1. Go to your GitHub repository
2. Click green "Code" button  
3. Select "Download ZIP"
4. Extract and deploy using this guide

**All documentation, code, and deployment files are included!**