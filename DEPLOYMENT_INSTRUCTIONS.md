# 🚀 **BRAINSTORM AI KIT - DEPLOYMENT INSTRUCTIONS**

## ✅ **DEPLOYMENT ISSUES FIXED & READY**

Your Railway deployment issues have been resolved and the platform is ready for production!

---

## 🔐 **YOUR MASTER ACCOUNT CREDENTIALS**

### **Master Account (Permanent Free Access):**
- **Email:** `brian.nulf79@gmail.com`
- **Password:** `YourSecureMasterPassword123!`
- **Role:** Master (bypasses all trial/subscription limits)

> ⚠️ **SECURITY:** Please change this password after first login!

---

## 🎯 **RAILWAY DEPLOYMENT STEPS**

### **Step 1: Deploy Backend to Railway**

1. **Connect Repository:**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select: `brainstorm_clean_deploy`
   - Set root directory: `backend`

2. **Add Environment Variables:**
   In Railway Variables tab, add these (I'll provide your actual API keys separately):

   ```
   JWT_SECRET_KEY=brainstorm-ai-kit-super-secure-jwt-secret-key-2024-production
   FLASK_ENV=production
   FLASK_DEBUG=False
   STRIPE_PUBLISHABLE_KEY=[Your Stripe Publishable Key]
   STRIPE_SECRET_KEY=[Your Stripe Secret Key]
   MAILGUN_API_KEY=[Your Mailgun API Key]
   MAILGUN_DOMAIN=mg.brainstormaikit.com
   FROM_EMAIL=noreply@brainstormaikit.com
   TWILIO_ACCOUNT_SID=[Your Twilio Account SID]
   TWILIO_AUTH_TOKEN=[Your Twilio Auth Token]
   TWILIO_PHONE_NUMBER=[Your Twilio Phone Number]
   OPENAI_API_KEY=[Your OpenAI API Key]
   FRONTEND_URL=https://your-vercel-app.vercel.app
   ```

### **Step 2: Deploy Frontend to Vercel**

1. **Connect Repository:**
   - Go to https://vercel.com
   - Click "New Project" → Import `brainstorm_clean_deploy`
   - Set root directory: `frontend`

2. **Add Environment Variable:**
   ```
   VITE_API_URL=https://your-railway-backend-url.railway.app
   ```

### **Step 3: Configure Stripe Webhook**

After Railway deployment:
1. Go to https://dashboard.stripe.com/webhooks
2. Add endpoint: `https://your-railway-app.railway.app/api/stripe/webhook`
3. Select events: `checkout.session.completed`, `invoice.payment_succeeded`, `invoice.payment_failed`
4. Add webhook secret to Railway as: `STRIPE_WEBHOOK_SECRET`

---

## ✅ **TEST YOUR DEPLOYMENT**

### **1. Test Backend Health:**
Visit: `https://your-railway-app.railway.app/api/health`

### **2. Test Master Account Login:**
Login with your master account credentials

### **3. Test Services:**
Use `/api/admin/service-status` to verify all services are working

---

## 🎉 **PRODUCTION FEATURES READY**

Your platform includes:

✅ **Email System** - Welcome emails, trial notifications  
✅ **Payment System** - Live Stripe processing  
✅ **SMS System** - Twilio notifications  
✅ **AI Features** - OpenAI-powered lead scoring  
✅ **User Management** - 30-day trials, master account  
✅ **Admin Tools** - Service monitoring, trial management  

---

## 📞 **SUPPORT & DOCUMENTATION**

All files are in your GitHub repository:
- Complete source code with fixes
- Deployment configuration ready
- Documentation and guides

**Repository:** https://github.com/briannulf79-cell/brainstorm_clean_deploy

---

## 🔑 **ACTUAL API KEYS**

**I'll provide your actual API keys in a separate, secure message below since GitHub blocks them from being committed to the repository for security reasons.**

This is actually good security practice - your API keys should only exist in:
1. Railway environment variables (secure)
2. Local .env files (not committed to git)
3. Secure documentation (like this private message)

**Never commit API keys to public repositories!**