# Multi-Tenant HRMS SaaS Platform - Frontend

Professional Next.js frontend for the HRMS SaaS platform with custom design system.

## Features

- ✅ Next.js 15 with App Router
- ✅ TypeScript for type safety
- ✅ Tailwind CSS with custom design system
- ✅ Custom color palette (#B85042, #E7E8D1, #A7BEAE)
- ✅ Professional animations
- ✅ JWT authentication
- ✅ Role-based routing
- ✅ Responsive design

## Color Palette

- **Primary**: `#B85042` - Warm terracotta for primary actions
- **Secondary**: `#A7BEAE` - Sage green for secondary elements
- **Accent**: `#E7E8D1` - Soft cream for backgrounds and accents

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.local.example .env.local
# Edit .env.local with your API URL
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── auth/              # Authentication pages
│   ├── employee/          # Employee dashboard
│   ├── hr/                # HR dashboard
│   ├── manager/           # Manager dashboard
│   └── globals.css        # Global styles
├── components/            # Reusable components
├── contexts/              # React contexts
├── services/              # API services
├── lib/                   # Utilities
├── types/                 # TypeScript types
└── config/                # Configuration
```

## Design System

### Components

- **Buttons**: `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-outline`
- **Cards**: `.card`, `.card-hover`
- **Inputs**: `.input`, `.input-error`
- **Badges**: `.badge`, `.badge-primary`, `.badge-success`

### Animations

- `animate-fade-in` - Fade in effect
- `animate-fade-in-up` - Fade in from bottom
- `animate-slide-in-left` - Slide from left
- `animate-scale-in` - Scale up effect
- `animate-pulse-subtle` - Subtle pulse

## Authentication

The app uses JWT-based authentication with automatic token refresh.

### Login

```typescript
const { login } = useAuth();
await login({ email, password });
```

### Protected Routes

Use the `useAuth` hook to check authentication status:

```typescript
const { isAuthenticated, user } = useAuth();
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## License

Proprietary - All Rights Reserved
