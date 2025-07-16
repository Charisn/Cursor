"use client"

import { useState } from "react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Separator } from "@/components/ui/separator"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { 
  Search,
  Filter,
  MoreHorizontal,
  Reply,
  Forward,
  Archive,
  Trash2,
  Star,
  Clock,
  CheckCircle,
  AlertCircle,
  Mail,
  Bot,
  User,
  Calendar,
  DollarSign,
  MapPin,
  Users,
  Bed
} from "lucide-react"
import { PremiumSidebar } from "@/components/premium-sidebar"
import { useAppStore } from "@/lib/store"
import { formatDate, formatTime } from "@/lib/utils"

export default function EmailsPage() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [selectedEmail, setSelectedEmail] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [filterStatus, setFilterStatus] = useState("all")
  
  const { emailQueries } = useAppStore()

  // Mock email data with more detailed content
  const emails = [
    {
      id: "1",
      from: "john.doe@email.com",
      fromName: "John Doe",
      subject: "Weekend Getaway Inquiry",
      preview: "Hi there! I'm looking for a room for 2 guests from March 15-17. Could you please check availability and send pricing?",
      content: `Hi there!

I'm planning a weekend getaway with my partner and I'm interested in booking a room at your hotel. Here are the details:

• Check-in: March 15, 2024
• Check-out: March 17, 2024
• Guests: 2 adults
• Room preference: King bed or queen bed
• Special requests: High floor if possible, quiet room

Could you please check availability and send me the pricing? Also, do you have any special weekend packages or amenities included?

I'd also like to know about:
- Parking availability
- Breakfast options
- Cancellation policy
- Pet policy (we might bring our small dog)

Looking forward to hearing from you!

Best regards,
John Doe
Phone: +1 (555) 123-4567`,
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
      status: "pending",
      priority: "high",
      aiProcessed: false,
      bookingGenerated: false,
      guestCount: 2,
      checkIn: "2024-03-15",
      checkOut: "2024-03-17",
      roomType: "King Suite",
      estimatedValue: 450
    },
    {
      id: "2",
      from: "sarah.wilson@company.com",
      fromName: "Sarah Wilson",
      subject: "Corporate Event Accommodation",
      preview: "We need to book 8 rooms for our company retreat from April 20-22. Please provide group rates and availability.",
      content: `Hello,

I'm reaching out regarding accommodation for our annual company retreat. We're looking to book multiple rooms for our team.

Requirements:
• Dates: April 20-22, 2024 (2 nights)
• Rooms needed: 8 rooms
• Guests: 12 people total (some single occupancy, some double)
• Meeting room: 1 conference room for 15 people
• Catering: Breakfast and lunch for all days

We're particularly interested in:
- Group discount rates
- Block booking arrangements
- Meeting facilities and AV equipment
- Team building activity recommendations
- Transportation from airport

Budget considerations are important for us, so please include your best corporate rates. We've been customers before and would appreciate loyalty pricing if available.

Please let me know what packages you can offer for corporate groups.

Best regards,
Sarah Wilson
Corporate Events Manager
TechCorp Solutions
sarah.wilson@company.com
Direct: +1 (555) 987-6543`,
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
      status: "responded",
      priority: "high",
      aiProcessed: true,
      bookingGenerated: true,
      guestCount: 12,
      checkIn: "2024-04-20",
      checkOut: "2024-04-22",
      roomType: "Multiple Rooms",
      estimatedValue: 3200
    },
    {
      id: "3",
      from: "mike.johnson@email.com",
      fromName: "Mike Johnson",
      subject: "Last Minute Booking",
      preview: "Need a room for tonight if available. Single occupancy, non-smoking. Can pay immediately upon confirmation.",
      content: `Hi,

I need a room for tonight (urgent) if you have availability. Travel plans changed at the last minute.

Details:
• Tonight only (1 night)
• 1 guest
• Non-smoking room
• Check-in around 8 PM
• Check-out tomorrow morning around 10 AM

I can pay immediately upon confirmation. Please let me know ASAP if you have anything available.

Thanks,
Mike Johnson
+1 (555) 456-7890`,
      timestamp: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
      status: "urgent",
      priority: "critical",
      aiProcessed: true,
      bookingGenerated: false,
      guestCount: 1,
      checkIn: new Date().toISOString().split('T')[0],
      checkOut: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      roomType: "Standard Room",
      estimatedValue: 120
    },
    {
      id: "4",
      from: "lisa.garcia@email.com",
      fromName: "Lisa Garcia",
      subject: "Anniversary Celebration",
      preview: "Booking for our 10th wedding anniversary. Looking for romantic package with special amenities.",
      content: `Dear Hotel Team,

My husband and I are celebrating our 10th wedding anniversary and would love to stay at your beautiful hotel.

We're looking for:
• Dates: May 14-16, 2024 (2 nights)
• 2 guests
• Romantic suite or room with special amenities
• Anniversary package if available
• Dinner reservations
• Spa services

Special requests:
- Champagne and flowers in room
- Late check-out if possible
- Quiet, romantic setting
- View room preferred

This is a very special occasion for us, so we're looking for the full experience. Please let me know what romantic packages you offer and the pricing.

With love and excitement,
Lisa Garcia
lisa.garcia@email.com
+1 (555) 321-9876`,
      timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
      status: "responded",
      priority: "medium",
      aiProcessed: true,
      bookingGenerated: true,
      guestCount: 2,
      checkIn: "2024-05-14",
      checkOut: "2024-05-16",
      roomType: "Romantic Suite",
      estimatedValue: 680
    },
    {
      id: "5",
      from: "david.brown@family.com",
      fromName: "David Brown",
      subject: "Family Vacation Planning",
      preview: "Family of 5 looking for connecting rooms or family suite for summer vacation. Kids ages 8, 12, and 15.",
      content: `Hello,

We're planning our family summer vacation and your hotel came highly recommended.

Our family details:
• 2 adults + 3 children (ages 8, 12, 15)
• Dates: July 10-17, 2024 (7 nights)
• Need: Connecting rooms or family suite
• Pool access essential
• Kid-friendly amenities

Requirements:
- Safe area for children
- Swimming pool with lifeguard
- Family activities nearby
- Breakfast included preferred
- Parking for SUV

The kids are excited about this trip, so we want to make sure there are activities for all age groups. Do you have any family packages or kids-stay-free deals?

Also interested in:
- Babysitting services
- Kids' club activities
- Family dining options
- Laundry facilities

Please send information about family-friendly accommodations and rates.

Best regards,
The Brown Family
David Brown (dad)
+1 (555) 654-3210`,
      timestamp: new Date(Date.now() - 12 * 60 * 60 * 1000), // 12 hours ago
      status: "pending",
      priority: "medium",
      aiProcessed: false,
      bookingGenerated: false,
      guestCount: 5,
      checkIn: "2024-07-10",
      checkOut: "2024-07-17",
      roomType: "Family Suite",
      estimatedValue: 1890
    }
  ]

  const filteredEmails = emails.filter(email => {
    const matchesSearch = email.fromName.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         email.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         email.preview.toLowerCase().includes(searchQuery.toLowerCase())
    
    if (filterStatus === "all") return matchesSearch
    return matchesSearch && email.status === filterStatus
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case "pending": return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100"
      case "responded": return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100"
      case "urgent": return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100"
      default: return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200"
    }
  }

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case "critical": return <AlertCircle className="h-4 w-4 text-red-500" />
      case "high": return <Star className="h-4 w-4 text-orange-500" />
      case "medium": return <Clock className="h-4 w-4 text-blue-500" />
      default: return <Mail className="h-4 w-4 text-gray-400" />
    }
  }

  const selectedEmailData = emails.find(email => email.id === selectedEmail)

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <PremiumSidebar 
        collapsed={sidebarCollapsed} 
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)} 
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Email Management
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Manage all guest inquiries and AI responses
              </p>
            </div>
            
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search emails..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 w-64"
                />
              </div>
              
              <Button variant="outline" size="sm">
                <Filter className="h-4 w-4 mr-2" />
                Filter
              </Button>
              
              <Button size="sm">
                <Reply className="h-4 w-4 mr-2" />
                Compose
              </Button>
            </div>
          </div>
        </header>

        <div className="flex-1 flex overflow-hidden">
          {/* Email List */}
          <div className="w-96 border-r border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
            {/* Filter Tabs */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-800">
              <Tabs value={filterStatus} onValueChange={setFilterStatus}>
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="all" className="text-xs">All</TabsTrigger>
                  <TabsTrigger value="pending" className="text-xs">Pending</TabsTrigger>
                  <TabsTrigger value="responded" className="text-xs">Responded</TabsTrigger>
                  <TabsTrigger value="urgent" className="text-xs">Urgent</TabsTrigger>
                </TabsList>
              </Tabs>
            </div>

            {/* Email List */}
            <div className="overflow-y-auto">
              {filteredEmails.map((email) => (
                <div
                  key={email.id}
                  onClick={() => setSelectedEmail(email.id)}
                  className={`p-4 border-b border-gray-100 dark:border-gray-800 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 ${
                    selectedEmail === email.id ? "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800" : ""
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <Avatar className="h-8 w-8">
                        <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-600 text-white text-xs">
                          {email.fromName.split(' ').map(n => n[0]).join('')}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                          {email.fromName}
                        </p>
                        <p className="text-xs text-gray-500 truncate">
                          {email.from}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-1">
                      {getPriorityIcon(email.priority)}
                      <span className="text-xs text-gray-500">
                        {formatTime(email.timestamp)}
                      </span>
                    </div>
                  </div>
                  
                  <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-1 truncate">
                    {email.subject}
                  </h3>
                  
                  <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2 mb-2">
                    {email.preview}
                  </p>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Badge className={`text-xs ${getStatusColor(email.status)}`}>
                        {email.status}
                      </Badge>
                      {email.aiProcessed && (
                        <Badge className="text-xs bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100">
                          <Bot className="h-3 w-3 mr-1" />
                          AI
                        </Badge>
                      )}
                    </div>
                    <div className="flex items-center space-x-1 text-xs text-gray-500">
                      <Users className="h-3 w-3" />
                      <span>{email.guestCount}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Email Detail */}
          <div className="flex-1 bg-white dark:bg-gray-900">
            {selectedEmailData ? (
              <div className="h-full flex flex-col">
                {/* Email Header */}
                <div className="p-6 border-b border-gray-200 dark:border-gray-800">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <Avatar className="h-12 w-12">
                        <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-600 text-white">
                          {selectedEmailData.fromName.split(' ').map(n => n[0]).join('')}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                          {selectedEmailData.fromName}
                        </h2>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {selectedEmailData.from}
                        </p>
                        <p className="text-xs text-gray-500">
                          {formatDate(selectedEmailData.timestamp)} at {formatTime(selectedEmailData.timestamp)}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Button variant="outline" size="sm">
                        <Reply className="h-4 w-4 mr-2" />
                        Reply
                      </Button>
                      <Button variant="outline" size="sm">
                        <Forward className="h-4 w-4 mr-2" />
                        Forward
                      </Button>
                      <Button variant="outline" size="sm">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                    {selectedEmailData.subject}
                  </h3>
                  
                  <div className="flex items-center space-x-4">
                    <Badge className={`${getStatusColor(selectedEmailData.status)}`}>
                      {selectedEmailData.status}
                    </Badge>
                    <div className="flex items-center space-x-1 text-sm text-gray-600">
                      {getPriorityIcon(selectedEmailData.priority)}
                      <span className="capitalize">{selectedEmailData.priority} Priority</span>
                    </div>
                    {selectedEmailData.aiProcessed && (
                      <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100">
                        <Bot className="h-3 w-3 mr-1" />
                        AI Processed
                      </Badge>
                    )}
                  </div>
                </div>

                {/* Booking Details */}
                <div className="p-6 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                  <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-3">Booking Details</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="flex items-center space-x-2">
                      <Calendar className="h-4 w-4 text-gray-500" />
                      <div>
                        <p className="text-xs text-gray-500">Check-in</p>
                        <p className="text-sm font-medium">{selectedEmailData.checkIn}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Calendar className="h-4 w-4 text-gray-500" />
                      <div>
                        <p className="text-xs text-gray-500">Check-out</p>
                        <p className="text-sm font-medium">{selectedEmailData.checkOut}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Users className="h-4 w-4 text-gray-500" />
                      <div>
                        <p className="text-xs text-gray-500">Guests</p>
                        <p className="text-sm font-medium">{selectedEmailData.guestCount}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <DollarSign className="h-4 w-4 text-gray-500" />
                      <div>
                        <p className="text-xs text-gray-500">Est. Value</p>
                        <p className="text-sm font-medium">${selectedEmailData.estimatedValue}</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Email Content */}
                <div className="flex-1 p-6 overflow-y-auto">
                  <div className="prose prose-sm max-w-none dark:prose-invert">
                    <pre className="whitespace-pre-wrap font-sans text-gray-700 dark:text-gray-300 leading-relaxed">
                      {selectedEmailData.content}
                    </pre>
                  </div>
                </div>

                {/* Action Bar */}
                <div className="p-6 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-800">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Button size="sm" className="bg-blue-600 text-white hover:bg-blue-700">
                        <Bot className="h-4 w-4 mr-2" />
                        Generate AI Response
                      </Button>
                      {selectedEmailData.bookingGenerated && (
                        <Link href="/booking/grand-plaza-deluxe-december">
                          <Button variant="outline" size="sm">
                            <Bed className="h-4 w-4 mr-2" />
                            View Booking Link
                          </Button>
                        </Link>
                      )}
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Button variant="outline" size="sm">
                        <Archive className="h-4 w-4 mr-2" />
                        Archive
                      </Button>
                      <Button variant="outline" size="sm">
                        <Trash2 className="h-4 w-4 mr-2" />
                        Delete
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="text-center">
                  <Mail className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    Select an email
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Choose an email from the list to view its details
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
} 