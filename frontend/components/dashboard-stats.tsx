"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { 
  Mail, 
  TrendingUp, 
  Clock, 
  DollarSign, 
  CalendarCheck,
  Users 
} from "lucide-react"
import { formatCurrency } from "@/lib/utils"
import { DashboardStats } from "@/lib/types"

interface DashboardStatsProps {
  stats: DashboardStats
}

export function DashboardStatsComponent({ stats }: DashboardStatsProps) {
  const statsConfig = [
    {
      title: "Total Emails",
      value: stats.totalEmails.toLocaleString(),
      icon: Mail,
      description: `${stats.emailsToday} today`,
      trend: "+12% from last month",
    },
    {
      title: "Avg Response Time",
      value: `${stats.averageResponseTime}min`,
      icon: Clock,
      description: "Real-time processing",
      trend: "-23% improvement",
    },
    {
      title: "Conversion Rate",
      value: `${stats.bookingConversionRate}%`,
      icon: TrendingUp,
      description: "Email to booking",
      trend: "+5.2% this month",
    },
    {
      title: "Total Revenue",
      value: formatCurrency(stats.totalRevenue),
      icon: DollarSign,
      description: "This month",
      trend: "+18% from last month",
    },
    {
      title: "Active Bookings",
      value: stats.activeBookings.toString(),
      icon: CalendarCheck,
      description: "Current reservations",
      trend: "+8 this week",
    },
    {
      title: "Hotels Connected",
      value: "12",
      icon: Users,
      description: "Active properties",
      trend: "+2 this month",
    },
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
      {statsConfig.map((stat, index) => (
        <Card key={index} className="relative overflow-hidden">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              {stat.title}
            </CardTitle>
            <stat.icon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
            <p className="text-xs text-muted-foreground mt-1">
              {stat.description}
            </p>
            <Badge 
              variant="secondary" 
              className="mt-2 text-xs bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100"
            >
              {stat.trend}
            </Badge>
          </CardContent>
        </Card>
      ))}
    </div>
  )
} 