# StayDesk Frontend

This is the frontend application for StayDesk, built with Next.js, TypeScript, and Tailwind CSS.

## Getting Started

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Run the development server**
   ```bash
   npm run dev
   ```

3. **Open [http://localhost:3000](http://localhost:3000) in your browser**

## Project Structure

```
frontend/
├── app/                     # Next.js App Router
│   ├── booking/            # Booking pages
│   │   └── [slug]/         # Dynamic booking routes
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Dashboard homepage
│   └── globals.css         # Global styles
├── components/             # React components
│   ├── ui/                 # Reusable UI components
│   ├── dashboard-stats.tsx # Dashboard metrics
│   └── recent-emails.tsx   # Email list component
├── lib/                    # Utilities
│   ├── types.ts           # TypeScript definitions
│   ├── utils.ts           # Helper functions
│   └── store.ts           # Zustand state management
└── public/                # Static assets
```

## Key Features

### Dashboard (`/`)
- Performance metrics and analytics
- Recent email queries with AI responses
- Quick actions for hotel management
- Real-time booking status

### Booking Pages (`/booking/[slug]`)
- Dynamic booking links from email responses
- Multi-step booking process
- Secure payment integration
- Mobile-responsive design

## Technology Stack

- **Next.js 15.4.1** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS v4** - Utility-first CSS framework
- **Zustand** - Lightweight state management
- **Radix UI** - Headless UI components
- **Lucide React** - Beautiful icons
- **Zod** - Schema validation

## Development Guidelines

### Components
- Use functional components with TypeScript
- Implement proper error boundaries
- Follow the component structure pattern:
  ```tsx
  // Imports
  // Types/Interfaces
  // Component definition
  // Export
  ```

### Styling
- Use Tailwind CSS classes
- Mobile-first responsive design
- Consistent color and spacing system
- Dark mode support

### State Management
- Zustand for global state
- React hooks for local state
- Server components by default
- Client components only when needed

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your_stripe_key
```

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
