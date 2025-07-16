"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Separator } from "@/components/ui/separator"
import { 
  Mail, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  Send, 
  Eye,
  MoreHorizontal,
  Filter,
  Search
} from "lucide-react"
import { EmailQuery } from "@/lib/types"
import { formatDate } from "@/lib/utils"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface PremiumEmailActivityProps {
  emails: EmailQuery[]
  title?: string
}

export function PremiumEmailActivity({ 
  emails, 
  title = "Recent Email Activity" 
}: PremiumEmailActivityProps) {
  const getStatusConfig = (status: EmailQuery["responseStatus"]) => {
    switch (status) {
      case "sent":
        return {
          icon: CheckCircle,
          color: "text-emerald-600",
          bgColor: "bg-emerald-50 dark:bg-emerald-900/20",
          badgeColor: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-100"
        }
      case "draft":
        return {
          icon: Clock,
          color: "text-amber-600",
          bgColor: "bg-amber-50 dark:bg-amber-900/20",
          badgeColor: "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-100"
        }
      case "failed":
        return {
          icon: AlertCircle,
          color: "text-red-600",
          bgColor: "bg-red-50 dark:bg-red-900/20",
          badgeColor: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100"
        }
      default:
        return {
          icon: Mail,
          color: "text-gray-600",
          bgColor: "bg-gray-50 dark:bg-gray-800",
          badgeColor: "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200"
        }
    }
  }

  const getInitials = (email: string) => {
    return email.split('@')[0].slice(0, 2).toUpperCase()
  }

  const getPriorityColor = (extractedInfo: EmailQuery["extractedInfo"]) => {
    if (extractedInfo.guests && extractedInfo.guests > 4) return "border-l-purple-500"
    if (extractedInfo.roomType?.toLowerCase().includes("suite")) return "border-l-blue-500"
    return "border-l-gray-200"
  }

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <Mail className="h-5 w-5 text-blue-600" />
            {title}
          </CardTitle>
          
          <div className="flex items-center gap-2">
            <Button size="sm" className="h-8 px-3 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
              <Filter className="h-3 w-3 mr-1" />
              Filter
            </Button>
            <Button size="sm" className="h-8 px-3 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
              <MoreHorizontal className="h-3 w-3" />
            </Button>
          </div>
        </div>
        
        {/* Search and filter controls */}
        <div className="flex items-center gap-3 mt-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input 
              placeholder="Search emails..." 
              className="pl-9 h-9 border-gray-200"
            />
          </div>
          <Select defaultValue="all">
            <SelectTrigger className="w-32 h-9">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="sent">Sent</SelectItem>
              <SelectItem value="draft">Draft</SelectItem>
              <SelectItem value="failed">Failed</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardHeader>
      
      <CardContent className="pt-0">
        <div className="space-y-4">
          {emails.slice(0, 6).map((email, index) => {
            const statusConfig = getStatusConfig(email.responseStatus)
            const StatusIcon = statusConfig.icon
            
            return (
              <div
                key={email.id}
                className={`group relative p-4 rounded-xl border-l-4 ${getPriorityColor(email.extractedInfo)} bg-gradient-to-r from-gray-50/50 to-transparent dark:from-gray-800/50 hover:from-gray-100/50 dark:hover:from-gray-700/50 transition-all duration-200 cursor-pointer`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3 flex-1">
                    {/* Avatar */}
                    <Avatar className="h-10 w-10 ring-2 ring-white shadow-sm">
                      <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-600 text-white text-sm font-medium">
                        {getInitials(email.senderEmail)}
                      </AvatarFallback>
                    </Avatar>
                    
                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="text-sm font-semibold text-foreground truncate pr-2">
                          {email.subject}
                        </h4>
                        <Badge className={`${statusConfig.badgeColor} border-0 text-xs capitalize flex items-center gap-1`}>
                          <StatusIcon className="h-3 w-3" />
                          {email.responseStatus}
                        </Badge>
                      </div>
                      
                      <p className="text-xs text-muted-foreground mb-2">
                        From: {email.senderEmail}
                      </p>
                      
                      {/* Extracted info tags */}
                      {(email.extractedInfo.checkIn || email.extractedInfo.guests || email.extractedInfo.roomType) && (
                        <div className="flex flex-wrap gap-2 mb-3">
                          {email.extractedInfo.checkIn && (
                            <Badge className="bg-blue-50 text-blue-700 dark:bg-blue-900/20 dark:text-blue-300 border-0 text-xs">
                              Check-in: {formatDate(email.extractedInfo.checkIn)}
                            </Badge>
                          )}
                          {email.extractedInfo.guests && (
                            <Badge className="bg-purple-50 text-purple-700 dark:bg-purple-900/20 dark:text-purple-300 border-0 text-xs">
                              {email.extractedInfo.guests} guests
                            </Badge>
                          )}
                          {email.extractedInfo.roomType && (
                            <Badge className="bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-300 border-0 text-xs">
                              {email.extractedInfo.roomType}
                            </Badge>
                          )}
                        </div>
                      )}
                      
                      {/* AI Response preview */}
                      <p className="text-xs text-muted-foreground line-clamp-2 mb-2">
                        {email.aiResponse}
                      </p>
                    </div>
                  </div>
                  
                  {/* Actions */}
                  <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                    <Button size="sm" className="h-7 px-2 border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
                      <Eye className="h-3 w-3" />
                    </Button>
                    {email.responseStatus === "draft" && (
                      <Button size="sm" className="h-7 px-2 bg-blue-600 text-white hover:bg-blue-700">
                        <Send className="h-3 w-3" />
                      </Button>
                    )}
                  </div>
                </div>
                
                {/* Timestamp */}
                <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-100 dark:border-gray-800">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <Clock className="h-3 w-3" />
                    <span>{formatDate(email.createdAt)}</span>
                  </div>
                  
                  {/* Response time indicator */}
                  <div className="text-xs text-muted-foreground">
                    Response time: 2.3 min
                  </div>
                </div>
                
                {index < emails.length - 1 && (
                  <Separator className="mt-4" />
                )}
              </div>
            )
          })}
        </div>
        
        {emails.length === 0 && (
          <div className="text-center py-12">
            <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
              <Mail className="h-8 w-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-foreground mb-1">No emails yet</h3>
            <p className="text-sm text-muted-foreground">Email responses will appear here when guests contact you</p>
          </div>
        )}
        
        {emails.length > 6 && (
          <div className="mt-6 text-center">
            <Button className="border border-gray-300 bg-white text-gray-700 hover:bg-gray-50">
              View All Emails ({emails.length})
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
} 