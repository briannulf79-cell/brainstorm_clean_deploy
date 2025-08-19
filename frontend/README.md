# Brainstorm AI Kit - Frontend

A modern, AI-powered CRM and marketing automation platform built with React 18, Vite, and Tailwind CSS.

## 🚀 Features

- **Modern React 18** with Vite for fast development
- **Tailwind CSS** for responsive, professional styling
- **Shadcn/UI Components** for consistent design system
- **React Router** for client-side routing
- **Recharts** for beautiful data visualizations
- **Lucide Icons** for consistent iconography
- **Environment Variable Support** for flexible configuration

## 📋 Prerequisites

- Node.js 18+ 
- pnpm (recommended) or npm
- Backend API running (see backend README)

## 🛠️ Installation

1. **Clone or extract the project**
   ```bash
   cd brainstorm-frontend-new
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```
   
   Edit `.env.local` and set your backend API URL:
   ```
   VITE_API_URL=http://localhost:5000
   ```

4. **Start development server**
   ```bash
   pnpm run dev
   ```

   The app will be available at `http://localhost:5173`

## 🚀 Deployment

### Vercel (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will auto-detect the Vite framework

3. **Set Environment Variables**
   In Vercel dashboard, add:
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   ```

4. **Deploy**
   - Vercel will automatically build and deploy
   - Your app will be live at `https://your-app.vercel.app`

### Other Platforms

The app can also be deployed to:
- Netlify
- AWS Amplify
- Firebase Hosting
- Any static hosting service

## 🔧 Build Commands

- **Development**: `pnpm run dev`
- **Build**: `pnpm run build`
- **Preview**: `pnpm run preview`
- **Lint**: `pnpm run lint`

## 📁 Project Structure

```
src/
├── components/          # React components
│   ├── ui/             # Shadcn/UI components
│   ├── Login.jsx       # Authentication
│   ├── Layout.jsx      # Main layout
│   ├── Dashboard.jsx   # Dashboard page
│   └── Contacts.jsx    # Contacts management
├── config.js           # API configuration
├── App.jsx            # Main app component
├── App.css            # Global styles
└── main.jsx           # App entry point
```

## 🔐 Authentication

The app supports:
- **Email/Password Login**
- **30-Day Free Trial Signup**
- **Demo Account Access**
- **JWT Token Management**

Demo credentials:
- Email: `admin@brainstormaikit.com`
- Password: `demo123`

## 🎨 Styling

- **Tailwind CSS** for utility-first styling
- **CSS Variables** for theme customization
- **Dark Mode Support** (built-in)
- **Responsive Design** for all screen sizes

## 🔌 API Integration

The frontend communicates with the backend via REST API:
- **Base URL**: Configured via `VITE_API_URL`
- **Authentication**: JWT tokens in localStorage
- **Error Handling**: Graceful fallbacks and user feedback

## 🐛 Troubleshooting

### Build Errors
- Ensure Node.js 18+ is installed
- Clear node_modules: `rm -rf node_modules && pnpm install`
- Check environment variables are set correctly

### API Connection Issues
- Verify `VITE_API_URL` points to your backend
- Check backend is running and accessible
- Verify CORS is configured on backend

### Deployment Issues
- Ensure all environment variables are set in deployment platform
- Check build logs for specific errors
- Verify `vercel.json` configuration is correct

## 📝 License

© 2024 Brainstorm AI Kit. All rights reserved.

## 🤝 Support

For support and questions, please refer to the main project documentation.

