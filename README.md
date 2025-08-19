# Brainstorm AI Kit

## 🧠 AI-Powered CRM & Marketing Automation Platform

A comprehensive business platform that rivals Go High Level with advanced AI integration, 30-day free trials, and white-label capabilities.

### 🚀 Quick Deploy

This repository contains the complete source code for both frontend and backend.

#### Frontend (React/Vite)
- Location: `/frontend`
- Deploy to: **Vercel**
- Framework: React + Vite + TailwindCSS

#### Backend (Python/Flask)
- Location: `/backend` 
- Deploy to: **Railway**
- Framework: Flask + SQLAlchemy + PostgreSQL

### 📋 Deployment Steps

1. **Deploy Backend to Railway:**
   - Connect this repo to Railway
   - Select `/backend` as root directory
   - Add environment variables (see `.env.example`)
   - Railway will auto-detect Flask and deploy

2. **Deploy Frontend to Vercel:**
   - Connect this repo to Vercel
   - Select `/frontend` as root directory
   - Add `VITE_API_URL` environment variable
   - Vercel will auto-detect Vite and deploy

### 🔧 Environment Variables

#### Backend (Railway)
```
DATABASE_URL=postgresql://... (auto-provided by Railway)
JWT_SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

#### Frontend (Vercel)
```
VITE_API_URL=https://your-backend.railway.app
```

### ✅ Features

- 🧠 **AI-Powered CRM** - Smart lead scoring and insights
- 📧 **Marketing Automation** - Email, SMS, and workflow builder
- 📊 **Advanced Analytics** - Real-time dashboards and reporting
- 🌐 **Website Builder** - Unlimited websites with templates
- 👑 **White-Label Program** - Reseller capabilities
- 💰 **30-Day Free Trial** - No credit card required
- 🔒 **Enterprise Security** - JWT auth and data protection

### 🎯 Demo

- **Demo URL:** [Your deployed frontend URL]
- **Demo Login:** admin@brainstormaikit.com / demo123

### 📞 Support

For deployment help or questions, check the documentation in each folder.

---

**Built with ❤️ for entrepreneurs and agencies who want to compete with industry leaders.** 

