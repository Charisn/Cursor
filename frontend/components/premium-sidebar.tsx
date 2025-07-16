"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import {
  BrainCircuit,
  LayoutDashboard,
  Mail,
  Hotel,
  CreditCard,
  BarChart3,
  Settings,
  Users,
  Bell,
  HelpCircle,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Zap
} from "lucide-react"

interface SidebarProps {
  collapsed?: boolean
  onToggle?: () => void
}

export function PremiumSidebar({ collapsed = false, onToggle }: SidebarProps) {

  const mainNavItems = [
    {
      title: "Dashboard",
      href: "/dashboard",
      icon: LayoutDashboard,
      active: true,
      badge: null
    },
    {
      title: "Email Activity",
      href: "/emails",
      icon: Mail,
      active: false,
      badge: { count: 12, variant: "default" as const }
    },
    {
      title: "Hotels",
      href: "/hotels",
      icon: Hotel,
      active: false,
      badge: null
    },
    {
      title: "Bookings",
      href: "/bookings",
      icon: CreditCard,
      active: false,
      badge: { count: 3, variant: "destructive" as const }
    },
    {
      title: "Analytics",
      href: "/analytics",
      icon: BarChart3,
      active: false,
      badge: null
    },
    {
      title: "Team",
      href: "/team",
      icon: Users,
      active: false,
      badge: null
    }
  ]

  const secondaryNavItems = [
    {
      title: "Settings",
      href: "/settings",
      icon: Settings,
      active: false
    },
    {
      title: "Help Center",
      href: "/help",
      icon: HelpCircle,
      active: false
    }
  ]

  return (
    <div className={`${collapsed ? 'w-16' : 'w-64'} h-screen bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col transition-all duration-300 ease-in-out`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-800">
        <div className="flex items-center justify-between">
          {!collapsed && (
            <div className="flex items-center space-x-2">
              <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-purple-600">
                <BrainCircuit className="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  StayDesk
                </h1>
                <div className="flex items-center gap-1">
                  <Sparkles className="h-3 w-3 text-blue-500" />
                  <span className="text-xs text-muted-foreground">AI-Powered</span>
                </div>
              </div>
            </div>
          )}
          
          <Button
            size="sm"
            className="h-8 w-8 p-0 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50"
            onClick={onToggle}
          >
            {collapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <ChevronLeft className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>

      {/* User Profile */}
      {!collapsed && (
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <div className="flex items-center space-x-3">
            <Avatar className="h-10 w-10 ring-2 ring-blue-100">
              <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-600 text-white text-sm font-medium">
                JD
              </AvatarFallback>
            </Avatar>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-foreground truncate">
                John Doe
              </p>
              <p className="text-xs text-muted-foreground truncate">
                Hotel Manager
              </p>
            </div>
            <Badge className="bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-100 text-xs">
              Pro
            </Badge>
          </div>
        </div>
      )}

      {/* AI Status */}
      {!collapsed && (
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-3">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-foreground">AI Active</span>
              </div>
              <Zap className="h-4 w-4 text-blue-600" />
            </div>
            <p className="text-xs text-muted-foreground">
              Processing 23 emails • 2.3min avg response
            </p>
          </div>
        </div>
      )}

      {/* Main Navigation */}
      <nav className="flex-1 overflow-y-auto p-4">
        <div className="space-y-1">
          {mainNavItems.map((item) => {
            const Icon = item.icon
            return (
              <Link key={item.href} href={item.href}>
                <div className={`group flex items-center justify-between w-full p-3 text-sm font-medium rounded-lg transition-all duration-200 ${
                  item.active
                    ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white'
                }`}>
                  <div className="flex items-center space-x-3">
                    <Icon className={`h-5 w-5 ${item.active ? 'text-blue-600' : 'text-gray-500 group-hover:text-gray-700'}`} />
                    {!collapsed && (
                      <span className="truncate">{item.title}</span>
                    )}
                  </div>
                  
                  {!collapsed && item.badge && (
                    <Badge 
                      className={`text-xs ${
                        item.badge.variant === 'destructive' 
                          ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100'
                          : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'
                      }`}
                    >
                      {item.badge.count}
                    </Badge>
                  )}
                </div>
              </Link>
            )
          })}
        </div>
        
        <Separator className="my-4" />
        
        <div className="space-y-1">
          {secondaryNavItems.map((item) => {
            const Icon = item.icon
            return (
              <Link key={item.href} href={item.href}>
                <div className="group flex items-center w-full p-3 text-sm font-medium text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white transition-all duration-200">
                  <Icon className="h-5 w-5 text-gray-500 group-hover:text-gray-700 mr-3" />
                  {!collapsed && (
                    <span className="truncate">{item.title}</span>
                  )}
                </div>
              </Link>
            )
          })}
        </div>
      </nav>

      {/* Footer */}
      {!collapsed && (
        <div className="p-4 border-t border-gray-200 dark:border-gray-800">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-3 text-white">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium">Upgrade to Pro</span>
              <Sparkles className="h-4 w-4" />
            </div>
            <p className="text-xs text-blue-100 mb-3">
              Unlock advanced AI features and analytics
            </p>
            <Button size="sm" className="w-full bg-white text-blue-600 hover:bg-blue-50 text-xs font-medium">
              Upgrade Now
            </Button>
          </div>
        </div>
      )}
    </div>
  )
} 