# 🔐 Environment Variables Configuration

This document lists all required environment variables for the Brainstorm AI Kit platform.

## 📋 Backend Environment Variables (.env)

Copy these variables to your `backend/.env` file and update with your actual API keys:

### 🗄️ Database Configuration
```bash
# Database URL (Railway provides this automatically)
DATABASE_URL=postgresql://username:password@host:port/database
```

### 🔑 JWT & Security
```bash
# JWT Secret Key (generate a secure random string)
JWT_SECRET_KEY=your-super-secret-jwt-key-here

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
```

### 💳 Stripe Configuration (Payments)
```bash
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

### 📧 Email Configuration (Mailgun)
```bash
MAILGUN_API_KEY=your_mailgun_api_key
MAILGUN_DOMAIN=your_mailgun_domain
FROM_EMAIL=noreply@brainstormaikit.com
```

### 📱 SMS Configuration (Twilio)
```bash
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

### 🤖 AI Configuration (OpenAI)
```bash
OPENAI_API_KEY=sk-your_openai_api_key
```

### 🌐 Frontend Configuration
```bash
# Frontend URL for redirects
FRONTEND_URL=https://app.brainstormaikit.com
```

## 🖥️ Frontend Environment Variables (.env)

Create a `.env` file in the `frontend` directory:

```bash
# Backend API URL
VITE_API_URL=https://your-backend.railway.app
```

## 📝 Notes

### Required API Keys
1. **Mailgun**: Sign up at mailgun.com and get your API key and domain
2. **Stripe**: Get your secret keys from stripe.com dashboard
3. **Twilio**: Get account credentials from twilio.com console
4. **OpenAI**: Get API key from platform.openai.com

### Security Considerations
- Use `sk_live_` keys for production Stripe
- Keep all keys secure and never commit to version control
- Use strong, unique JWT secret keys
- Consider using environment-specific configurations

### Railway Deployment
- Railway automatically provides `DATABASE_URL`
- Add other environment variables in Railway dashboard
- Use Railway's environment variable UI for secure key management

### Vercel Deployment
- Add `VITE_API_URL` in Vercel dashboard
- Point to your Railway backend URL
- Ensure CORS is properly configured

## ✅ Testing Environment Variables

Use the admin endpoint to verify all services are properly configured:

```bash
GET /api/admin/service-status
```

This will show the status of all integrated services and help identify any configuration issues.