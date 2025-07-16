"use client"

import "@/app/globals.css"
import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { 
  BrainCircuit, 
  Mail, 
  Zap, 
  Shield, 
  Globe,
  ArrowRight,
  CheckCircle,
  Star,
  Users,
  Clock,
  TrendingUp,
  Play,
  ChevronRight,
  Sparkles,
  Building,
  MessageSquare,
  CreditCard,
  Send,
  ExternalLink,
  CalendarCheck
} from "lucide-react"

export default function LandingPage() {
  const [isVideoPlaying, setIsVideoPlaying] = useState(false)

  const features = [
    {
      icon: Mail,
      title: "Smart Email Processing",
      description: "AI automatically reads and understands guest inquiries, extracting key details like dates, guest count, and preferences.",
      color: "text-blue-600",
      bgColor: "bg-blue-100 dark:bg-blue-900/20"
    },
    {
      icon: Zap,
      title: "Instant Responses",
      description: "Generate personalized responses with real-time availability and pricing in seconds, not hours.",
      color: "text-yellow-600",
      bgColor: "bg-yellow-100 dark:bg-yellow-900/20"
    },
    {
      icon: Globe,
      title: "Secure Booking Links",
      description: "Send direct booking links that guide guests through a seamless, mobile-optimized reservation process.",
      color: "text-green-600",
      bgColor: "bg-green-100 dark:bg-green-900/20"
    },
    {
      icon: Shield,
      title: "24/7 Automation",
      description: "Never miss an inquiry. Our AI works around the clock to ensure every potential guest gets a timely response.",
      color: "text-purple-600",
      bgColor: "bg-purple-100 dark:bg-purple-900/20"
    }
  ]

  const benefits = [
    "Increase booking conversion rates by 40%",
    "Reduce response time from hours to minutes",
    "Handle unlimited email inquiries simultaneously",
    "Integrate with any email platform",
    "Multi-language support",
    "Secure payment processing"
  ]

  const testimonials = [
    {
      name: "Sarah Johnson",
      role: "Hotel Manager",
      hotel: "Grand Plaza Hotel",
      content: "StayDesk transformed our email management. We've seen a 45% increase in bookings since implementation.",
      rating: 5
    },
    {
      name: "Miguel Rodriguez",
      role: "Owner",
      hotel: "Seaside Resort",
      content: "The AI responses are so natural, guests don't even realize they're automated. It's incredible technology.",
      rating: 5
    },
    {
      name: "Emma Chen",
      role: "Operations Director",
      hotel: "City Center Inn",
      content: "We process 3x more inquiries with the same staff. StayDesk paid for itself in the first month.",
      rating: 5
    }
  ]

  const stats = [
    { label: "Hotels Using StayDesk", value: "500+", icon: Building },
    { label: "Emails Processed Daily", value: "10K+", icon: Mail },
    { label: "Average Response Time", value: "2.3min", icon: Clock },
    { label: "Booking Conversion Rate", value: "34%", icon: TrendingUp }
  ]

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900">
      {/* Navigation */}
      <nav className="border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-2">
              <BrainCircuit className="h-8 w-8 text-blue-600" />
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                StayDesk
              </span>
              <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100">
                AI-Powered
              </Badge>
            </div>
            
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors">Features</a>
              <a href="#how-it-works" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors">How it Works</a>
              <a href="#pricing" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors">Pricing</a>
              <Link href="/dashboard">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                  View Dashboard
                </Button>
              </Link>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <Link href="/dashboard">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                  Dashboard
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="text-center lg:text-left">
              <Badge className="inline-flex items-center gap-2 mb-6 bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100">
                <Sparkles className="h-3 w-3" />
                AI-Powered Email Management
              </Badge>
              
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 dark:text-white mb-6">
                Transform Your
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"> Hotel Emails </span>
                into Bookings
              </h1>
              
              <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl">
                StayDesk's AI automatically reads guest inquiries, provides instant availability and pricing, 
                and sends secure booking links—turning every email into a potential reservation.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <Link href="/dashboard">
                  <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg">
                    Try Free Demo
                    <ArrowRight className="h-5 w-5 ml-2" />
                  </Button>
                </Link>
                <Link href="/booking/grand-plaza-deluxe-december">
                  <Button 
                    size="lg" 
                    className="border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 px-8 py-4 text-lg"
                  >
                    <CalendarCheck className="h-5 w-5 mr-2" />
                    Test Booking
                  </Button>
                </Link>
              </div>
              
              <div className="flex items-center gap-6 mt-8">
                <div className="flex -space-x-2">
                  {[1, 2, 3, 4].map((i) => (
                    <div key={i} className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 border-2 border-white" />
                  ))}
                </div>
                <div>
                  <div className="flex items-center gap-1">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Trusted by 500+ hotels</p>
                </div>
              </div>
            </div>
            
            {/* Email Processing Flow Demo */}
            <div className="relative">
              <div className="relative space-y-4">
                {/* Incoming Email */}
                <Card className="relative bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg">
                  <CardContent className="p-4">
                    <div className="flex items-start gap-3">
                      <div className="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                        <span className="text-xs font-medium">JD</span>
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-medium">john.doe@email.com</span>
                          <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100 text-xs">
                            Received
                          </Badge>
                        </div>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                          Subject: Room availability for December
                        </p>
                        <p className="text-sm text-gray-800 dark:text-gray-200">
                          "Looking for a room Dec 15-18 for 2 guests. What are your rates?"
                        </p>
                        <div className="flex items-center gap-2 mt-2">
                          <Clock className="h-3 w-3 text-gray-400" />
                          <span className="text-xs text-gray-500">Just now</span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Processing Animation */}
                <div className="flex items-center justify-center py-2">
                  <div className="flex items-center gap-2 px-3 py-1 bg-blue-50 dark:bg-blue-900/20 rounded-full">
                    <BrainCircuit className="h-4 w-4 text-blue-600 animate-pulse" />
                    <span className="text-xs text-blue-600 font-medium">AI Processing...</span>
                  </div>
                </div>

                {/* AI Response */}
                <Card className="relative bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border border-green-200 dark:border-green-800 shadow-lg">
                  <CardContent className="p-4">
                    <div className="flex items-start gap-3">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                        <BrainCircuit className="h-4 w-4 text-white" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-medium">StayDesk AI</span>
                          <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100 text-xs">
                            <Send className="h-3 w-3 mr-1" />
                            Sent
                          </Badge>
                        </div>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                          Re: Room availability for December
                        </p>
                        <p className="text-sm text-gray-800 dark:text-gray-200 mb-3">
                          "Hello John! Thank you for your inquiry. We have availability for Dec 15-18. 
                          Our Deluxe King Room is $299/night for 2 guests, including breakfast."
                        </p>
                        
                        {/* Booking Link */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <CalendarCheck className="h-4 w-4 text-blue-600" />
                              <span className="text-sm font-medium">Secure Booking Link</span>
                            </div>
                            <Link href="/booking/grand-plaza-deluxe-december">
                              <Button size="sm" className="h-7 px-3 bg-blue-600 text-white hover:bg-blue-700">
                                <ExternalLink className="h-3 w-3 mr-1" />
                                Book Now
                              </Button>
                            </Link>
                          </div>
                          <p className="text-xs text-gray-500 mt-1">
                            Complete your reservation in 2 minutes
                          </p>
                        </div>
                        
                        <div className="flex items-center gap-2 mt-3">
                          <Clock className="h-3 w-3 text-green-500" />
                          <span className="text-xs text-green-600 font-medium">Responded in 1.2 minutes</span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Stats overlay */}
                <div className="absolute -right-4 top-1/2 transform -translate-y-1/2">
                  <Card className="bg-white dark:bg-gray-800 shadow-xl border border-gray-200 dark:border-gray-700 p-4 w-48">
                    <div className="space-y-3">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">2.3min</div>
                        <div className="text-xs text-gray-500">Avg Response Time</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">34%</div>
                        <div className="text-xs text-gray-500">Conversion Rate</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-purple-600">500+</div>
                        <div className="text-xs text-gray-500">Hotels Trust Us</div>
                      </div>
                    </div>
                  </Card>
                </div>
              </div>
              
              {/* Floating elements */}
              <div className="absolute -top-4 -left-4 bg-blue-600 text-white p-3 rounded-lg shadow-lg">
                <MessageSquare className="h-6 w-6" />
              </div>
              <div className="absolute -bottom-4 -right-4 bg-green-600 text-white p-3 rounded-lg shadow-lg">
                <CheckCircle className="h-6 w-6" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Powerful Features for Modern Hotels
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Everything you need to automate your email management and boost bookings
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="text-center border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
                <CardContent className="p-8">
                  <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full ${feature.bgColor} mb-6`}>
                    <feature.icon className={`h-8 w-8 ${feature.color}`} />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How it Works Section */}
      <section id="how-it-works" className="py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              How StayDesk Works
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              From inquiry to booking in three simple steps
            </p>
          </div>
          
          <div className="grid lg:grid-cols-3 gap-8">
            {[
              {
                step: "01",
                title: "Guest Sends Inquiry",
                description: "Guests email your hotel with booking questions and requirements",
                icon: Mail
              },
              {
                step: "02", 
                title: "AI Processes & Responds",
                description: "Our AI reads the email, checks availability, calculates pricing, and sends a personalized response",
                icon: BrainCircuit
              },
              {
                step: "03",
                title: "Guest Books Directly",
                description: "Guests click the secure booking link and complete their reservation instantly",
                icon: CreditCard
              }
            ].map((step, index) => (
              <div key={index} className="relative">
                <Card className="text-center p-8 h-full border-2 border-gray-100 dark:border-gray-800 hover:border-blue-200 dark:hover:border-blue-800 transition-colors">
                  <CardContent className="p-0">
                    <div className="relative mb-6">
                      <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-600 text-white mb-4">
                        <step.icon className="h-8 w-8" />
                      </div>
                      <Badge className="absolute -top-2 -right-2 bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100 text-xs font-mono">
                        {step.step}
                      </Badge>
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                      {step.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-300">
                      {step.description}
                    </p>
                  </CardContent>
                </Card>
                
                {index < 2 && (
                  <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                    <ChevronRight className="h-8 w-8 text-gray-300" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white mb-6">
                Why Hotels Choose StayDesk
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
                Join hundreds of hotels already transforming their email management with AI
              </p>
              
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0" />
                    <span className="text-gray-700 dark:text-gray-300">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="space-y-6">
              {testimonials.map((testimonial, index) => (
                <Card key={index} className="p-6 border-l-4 border-l-blue-600">
                  <CardContent className="p-0">
                    <div className="flex items-center gap-1 mb-3">
                      {[1, 2, 3, 4, 5].map((i) => (
                        <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      ))}
                    </div>
                    <p className="text-gray-600 dark:text-gray-300 mb-4 italic">
                      "{testimonial.content}"
                    </p>
                    <div>
                      <p className="font-semibold text-gray-900 dark:text-white">
                        {testimonial.name}
                      </p>
                      <p className="text-sm text-gray-500">
                        {testimonial.role}, {testimonial.hotel}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl lg:text-4xl font-bold text-white mb-6">
            Ready to Transform Your Hotel's Email Management?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Start your free trial today and see how StayDesk can boost your bookings
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/dashboard">
              <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 text-lg">
                Start Free Trial
                <ArrowRight className="h-5 w-5 ml-2" />
              </Button>
            </Link>
            <Button size="lg" className="border-2 border-white text-white hover:bg-white hover:text-blue-600 px-8 py-4 text-lg">
              Schedule Demo
            </Button>
          </div>
          
          <p className="text-blue-100 text-sm mt-6">
            No credit card required • 14-day free trial • Setup in 5 minutes
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <BrainCircuit className="h-6 w-6 text-blue-400" />
                <span className="text-xl font-bold">StayDesk</span>
              </div>
              <p className="text-gray-400">
                AI-powered email management for modern hotels.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#how-it-works" className="hover:text-white transition-colors">How it Works</a></li>
                <li><a href="#pricing" className="hover:text-white transition-colors">Pricing</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Status</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 StayDesk. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
