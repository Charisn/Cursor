"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { 
  Bell,
  Plus,
  RefreshCw,
  Download,
  MoreHorizontal,
  TrendingUp,
  TrendingDown,
  Users,
  Mail,
  DollarSign,
  Clock,
  Hotel,
  Zap,
  Target,
  Calendar,
  Globe,
  Filter
} from "lucide-react"
import { PremiumStatsCard } from "@/components/premium-stats-card"
import { PremiumChart } from "@/components/premium-chart"
import { PremiumEmailActivity } from "@/components/premium-email-activity"
import { PremiumSidebar } from "@/components/premium-sidebar"
import { useAppStore, mockStats } from "@/lib/store"
import { formatCurrency } from "@/lib/utils"

export default function PremiumDashboard() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const { 
    stats, 
    emailQueries, 
    bookings, 
    setStats, 
    setEmailQueries 
  } = useAppStore()

  // Mock data initialization
  useEffect(() => {
    setStats(mockStats)
    setEmailQueries([
      {
        id: "1",
        hotelId: "hotel-1",
        senderEmail: "john.doe@email.com",
        subject: "Booking Inquiry for December",
        content: "Hello, I would like to book a room for December 15-18 for 2 guests.",
        extractedInfo: {
          checkIn: new Date("2024-12-15"),
          checkOut: new Date("2024-12-18"),
          guests: 2,
          roomType: "Standard"
        },
        aiResponse: "Thank you for your inquiry! We have availability for December 15-18. Here are our options...",
        responseStatus: "sent",
        createdAt: new Date("2024-07-16T10:30:00")
      },
      {
        id: "2",
        hotelId: "hotel-1",
        senderEmail: "sarah.smith@company.com",
        subject: "Corporate Booking Request",
        content: "We need accommodation for our team of 6 people for next week.",
        extractedInfo: {
          guests: 6,
          roomType: "Business"
        },
        aiResponse: "Thank you for reaching out! For your corporate booking...",
        responseStatus: "draft",
        createdAt: new Date("2024-07-16T09:15:00")
      },
      {
        id: "3",
        hotelId: "hotel-1",
        senderEmail: "lisa.williams@vacation.com",
        subject: "Weekend Getaway Inquiry",
        content: "Looking for a romantic suite for our anniversary weekend.",
        extractedInfo: {
          guests: 2,
          roomType: "Suite",
          specialRequests: ["Anniversary", "Romantic"]
        },
        aiResponse: "Congratulations on your anniversary! We have the perfect romantic suite available...",
        responseStatus: "sent",
        createdAt: new Date("2024-07-16T08:45:00")
      }
    ])
  }, [setStats, setEmailQueries])

  // Mock chart data
  const emailChartData = [
    { name: "Mon", value: 45 },
    { name: "Tue", value: 52 },
    { name: "Wed", value: 48 },
    { name: "Thu", value: 61 },
    { name: "Fri", value: 67 },
    { name: "Sat", value: 58 },
    { name: "Sun", value: 43 },
  ]

  const revenueChartData = [
    { name: "Jan", value: 24500 },
    { name: "Feb", value: 28200 },
    { name: "Mar", value: 31800 },
    { name: "Apr", value: 29400 },
    { name: "May", value: 35600 },
    { name: "Jun", value: 38900 },
    { name: "Jul", value: 42100 },
  ]

  const conversionChartData = [
    { name: "Week 1", value: 32.5 },
    { name: "Week 2", value: 28.8 },
    { name: "Week 3", value: 35.2 },
    { name: "Week 4", value: 39.1 },
  ]

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <PremiumSidebar 
        collapsed={sidebarCollapsed} 
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)} 
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Dashboard Overview
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Monitor your hotel's AI-powered email performance
              </p>
            </div>
            
            <div className="flex items-center space-x-3">
              <Button className="h-9 px-4 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
              <Button className="h-9 px-4 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
              <Button className="h-9 px-4 bg-blue-600 text-white hover:bg-blue-700">
                <Plus className="h-4 w-4 mr-2" />
                Add Hotel
              </Button>
              
              <Separator orientation="vertical" className="h-6" />
              
              <Button className="h-9 w-9 p-0 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
                <Bell className="h-4 w-4" />
              </Button>
              
              <Avatar className="h-9 w-9 ring-2 ring-blue-100">
                <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-600 text-white text-sm font-medium">
                  JD
                </AvatarFallback>
              </Avatar>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            {/* Stats Cards */}
            {stats && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <PremiumStatsCard
                  title="Total Emails"
                  value={stats.totalEmails}
                  change="+12% vs last month"
                  changeType="positive"
                  icon={Mail}
                  description={`${stats.emailsToday} emails today`}
                  gradient="from-blue-500 to-blue-600"
                />
                <PremiumStatsCard
                  title="Response Time"
                  value={`${stats.averageResponseTime}min`}
                  change="-23% improvement"
                  changeType="positive"
                  icon={Clock}
                  description="Average AI response time"
                  progress={87}
                  gradient="from-emerald-500 to-emerald-600"
                />
                <PremiumStatsCard
                  title="Conversion Rate"
                  value={`${stats.bookingConversionRate}%`}
                  change="+5.2% this month"
                  changeType="positive"
                  icon={Target}
                  description="Email to booking ratio"
                  progress={stats.bookingConversionRate}
                  gradient="from-purple-500 to-purple-600"
                />
                <PremiumStatsCard
                  title="Revenue"
                  value={formatCurrency(stats.totalRevenue)}
                  change="+18% from last month"
                  changeType="positive"
                  icon={DollarSign}
                  description="This month's earnings"
                  gradient="from-orange-500 to-orange-600"
                />
              </div>
            )}

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              <PremiumChart
                title="Email Volume"
                description="Daily email inquiries processed"
                data={emailChartData}
                type="area"
                height={280}
                primaryColor="#3b82f6"
              />
              
              <PremiumChart
                title="Revenue Trend"
                description="Monthly revenue growth"
                data={revenueChartData}
                type="bar"
                height={280}
                primaryColor="#10b981"
              />
              
              <PremiumChart
                title="Conversion Rate"
                description="Weekly booking conversion"
                data={conversionChartData}
                type="line"
                height={280}
                primaryColor="#8b5cf6"
              />
            </div>

            {/* Main Content Tabs */}
            <Tabs defaultValue="activity" className="space-y-6">
              <div className="flex items-center justify-between">
                <TabsList className="grid w-fit grid-cols-3 bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
                  <TabsTrigger value="activity" className="px-6 py-2">Email Activity</TabsTrigger>
                  <TabsTrigger value="analytics" className="px-6 py-2">Analytics</TabsTrigger>
                  <TabsTrigger value="hotels" className="px-6 py-2">Hotels</TabsTrigger>
                </TabsList>
                
                <div className="flex items-center gap-2">
                  <Button className="h-8 px-3 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
                    <Filter className="h-3 w-3 mr-1" />
                    Filter
                  </Button>
                  <Button className="h-8 px-3 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
                    <MoreHorizontal className="h-3 w-3" />
                  </Button>
                </div>
              </div>

              <TabsContent value="activity" className="space-y-6">
                <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                  <div className="xl:col-span-2">
                    <PremiumEmailActivity emails={emailQueries} />
                  </div>
                  
                  <div className="space-y-6">
                    {/* AI Performance Card */}
                    <Card className="border-0 shadow-lg">
                      <CardHeader className="pb-4">
                        <CardTitle className="text-lg font-semibold flex items-center gap-2">
                          <Zap className="h-5 w-5 text-blue-600" />
                          AI Performance
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-6">
                        <div className="space-y-4">
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                Response Accuracy
                              </span>
                              <span className="text-sm font-bold text-gray-900 dark:text-white">96.8%</span>
                            </div>
                            <Progress value={96.8} className="h-2" />
                          </div>
                          
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                Processing Speed
                              </span>
                              <span className="text-sm font-bold text-gray-900 dark:text-white">2.1s</span>
                            </div>
                            <Progress value={92} className="h-2" />
                          </div>
                          
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                Customer Satisfaction
                              </span>
                              <span className="text-sm font-bold text-gray-900 dark:text-white">4.8/5</span>
                            </div>
                            <Progress value={95} className="h-2" />
                          </div>
                        </div>
                        
                        <Separator />
                        
                        <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-4">
                          <div className="flex items-center gap-2 mb-2">
                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                            <span className="text-sm font-medium">AI Status: Active</span>
                          </div>
                          <p className="text-xs text-muted-foreground">
                            Processing 23 emails in queue • Next batch in 45s
                          </p>
                        </div>
                      </CardContent>
                    </Card>

                    {/* Quick Actions Card */}
                    <Card className="border-0 shadow-lg">
                      <CardHeader className="pb-4">
                        <CardTitle className="text-lg font-semibold">Quick Actions</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <Button className="w-full justify-start h-11 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
                          <Mail className="h-4 w-4 mr-3" />
                          View All Emails
                          <Badge className="ml-auto bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100">
                            23
                          </Badge>
                        </Button>
                        
                        <Button className="w-full justify-start h-11 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
                          <Hotel className="h-4 w-4 mr-3" />
                          Manage Hotels
                        </Button>
                        
                        <Button className="w-full justify-start h-11 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
                          <Globe className="h-4 w-4 mr-3" />
                          Create Booking Link
                        </Button>
                        
                        <Separator />
                        
                        <div className="space-y-3">
                          <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">Recent Bookings</h4>
                          
                          {bookings.slice(0, 3).map((booking) => (
                            <div key={booking.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                              <div className="flex items-center space-x-3">
                                <Avatar className="h-8 w-8">
                                  <AvatarFallback className="bg-gradient-to-br from-green-500 to-emerald-600 text-white text-xs">
                                    {booking.guestName.split(' ').map(n => n[0]).join('')}
                                  </AvatarFallback>
                                </Avatar>
                                <div>
                                  <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                                    {booking.guestName}
                                  </p>
                                  <p className="text-xs text-gray-500">
                                    {formatCurrency(booking.totalPrice)}
                                  </p>
                                </div>
                              </div>
                              <Badge 
                                className={`text-xs ${
                                  booking.status === "confirmed" 
                                    ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-100" 
                                    : "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200"
                                }`}
                              >
                                {booking.status}
                              </Badge>
                            </div>
                          ))}
                          
                          {bookings.length === 0 && (
                            <p className="text-sm text-muted-foreground text-center py-4">
                              No recent bookings
                            </p>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="analytics" className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <Card className="border-0 shadow-lg">
                    <CardHeader>
                      <CardTitle>Performance Metrics</CardTitle>
                      <CardDescription>
                        Key performance indicators for the last 30 days
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium">Email Processing</span>
                          <span className="text-sm text-muted-foreground">1,247 emails</span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium">Successful Responses</span>
                          <span className="text-sm text-muted-foreground">1,201 (96.3%)</span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium">Bookings Generated</span>
                          <span className="text-sm text-muted-foreground">429 bookings</span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium">Revenue Generated</span>
                          <span className="text-sm text-muted-foreground">{formatCurrency(125420)}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                  
                  <Card className="border-0 shadow-lg">
                    <CardHeader>
                      <CardTitle>Top Performing Hotels</CardTitle>
                      <CardDescription>
                        Hotels with highest conversion rates
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {["Grand Plaza Hotel", "Seaside Resort", "City Center Inn"].map((hotel, index) => (
                          <div key={hotel} className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                              <span className="text-sm font-medium">{hotel}</span>
                            </div>
                            <span className="text-sm text-muted-foreground">
                              {[42.1, 38.7, 35.2][index]}%
                            </span>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              <TabsContent value="hotels" className="space-y-6">
                <Card className="border-0 shadow-lg">
                  <CardHeader>
                    <CardTitle>Connected Hotels</CardTitle>
                    <CardDescription>
                      Manage your hotel properties and their AI settings
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center py-12">
                      <Hotel className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                      <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                        Connect Your First Hotel
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
                        Add your hotel to start automating email responses
                      </p>
                      <Button className="bg-blue-600 text-white hover:bg-blue-700">
                        <Plus className="h-4 w-4 mr-2" />
                        Add Hotel
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    </div>
  )
} 