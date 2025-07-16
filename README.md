# StayDesk - AI-Powered Hotel Email Management

🏨 **StayDesk** is an intelligent email management system for hotels that automatically reads guest inquiries, provides real-time availability and pricing, and generates secure booking links - all powered by AI.

## ✨ Features

### 🤖 AI-Powered Email Processing
- **Automatic Email Reading**: Parse guest inquiries from any email platform
- **Intelligent Data Extraction**: Extract check-in/out dates, guest count, room preferences
- **Context Understanding**: Understand guest intent and special requests

### ⚡ Real-Time Responses
- **Instant Availability Check**: Real-time room availability lookup
- **Dynamic Pricing**: Automatic pricing calculation based on dates and occupancy
- **Personalized Responses**: Tailored email responses for each inquiry

### 🔗 Secure Booking Links
- **One-Click Booking**: Direct booking links sent in email responses
- **Secure Payment Processing**: Industry-standard payment security
- **Mobile-Optimized**: Responsive booking pages for all devices

### 📊 Dashboard & Analytics
- **Performance Metrics**: Track response times, conversion rates, revenue
- **Email Management**: Monitor all inquiries and responses
- **Booking Tracking**: Real-time booking status and management

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/staydesk.git
   cd staydesk
   ```

2. **Install dependencies**
   ```bash
   npm run install-deps
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🏗️ Project Structure

```
staydesk/
├── frontend/                 # Next.js React application
│   ├── app/                 # App router pages
│   │   ├── booking/         # Dynamic booking pages
│   │   │   └── [slug]/      # Booking link handler
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Dashboard landing page
│   ├── components/          # Reusable UI components
│   │   ├── ui/              # Base UI components
│   │   ├── dashboard-stats.tsx
│   │   └── recent-emails.tsx
│   ├── lib/                 # Utilities and configurations
│   │   ├── types.ts         # TypeScript definitions
│   │   ├── utils.ts         # Helper functions
│   │   └── store.ts         # State management (Zustand)
│   └── package.json
├── backend/                 # Future API services
│   ├── api/                 # REST API endpoints
│   └── nlp/                 # AI/NLP processing
└── package.json             # Root package configuration
```

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 15.4.1 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **State Management**: Zustand
- **UI Components**: Radix UI + Custom components
- **Icons**: Lucide React
- **Validation**: Zod

### Backend (Future)
- **Runtime**: Node.js / Python
- **AI/NLP**: OpenAI GPT / Custom models
- **Database**: PostgreSQL / MongoDB
- **Email Integration**: IMAP/POP3 connectors

## 📱 Usage

### Dashboard Overview
The main dashboard provides:
- **Performance metrics** (emails processed, response times, conversions)
- **Recent email queries** with AI-generated responses
- **Quick actions** for hotel management and settings
- **Real-time booking status** tracking

### Email Processing Flow
1. **Guest sends inquiry** to hotel email
2. **AI processes** email content and extracts booking details
3. **System checks** availability and calculates pricing
4. **Automated response** sent with booking link
5. **Guest completes** booking via secure link

### Booking Page Features
- **Multi-step booking process** (details → payment → confirmation)
- **Real-time pricing** calculation
- **Secure payment** processing
- **Mobile-responsive** design
- **Guest information** validation

## 🔧 Development

### Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint

# Dependencies
npm run install-deps # Install frontend dependencies
```

### Component Development
- Use **TypeScript** for all components
- Follow **functional component** patterns
- Implement **proper error handling**
- Add **JSDoc comments** for complex logic
- Use **Tailwind CSS** for styling

### State Management
- **Zustand store** for global state
- **React hooks** for local state
- **Server components** when possible
- **Client components** only when needed

## 🚀 Deployment

### Vercel (Recommended)
1. Connect repository to Vercel
2. Set build command: `cd frontend && npm run build`
3. Set output directory: `frontend/.next`
4. Deploy automatically on push

### Docker
```bash
# Build image
docker build -t staydesk .

# Run container
docker run -p 3000:3000 staydesk
```

## 🔮 Roadmap

### Phase 1: Core MVP ✅
- [x] Landing page dashboard
- [x] Booking page with dynamic routing
- [x] UI components and responsive design
- [x] TypeScript implementation

### Phase 2: AI Integration
- [ ] Email parsing and NLP processing
- [ ] AI response generation
- [ ] Real-time availability checking
- [ ] Dynamic pricing engine

### Phase 3: Backend Services
- [ ] REST API development
- [ ] Database integration
- [ ] Email platform connectors
- [ ] Payment processing

### Phase 4: Advanced Features
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Mobile app
- [ ] Hotel management portal

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Documentation**: [docs.staydesk.com](https://docs.staydesk.com)
- **Issues**: [GitHub Issues](https://github.com/your-org/staydesk/issues)
- **Email**: support@staydesk.com

---

Built with ❤️ by the StayDesk Team