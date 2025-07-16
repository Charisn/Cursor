"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Mail, Clock, CheckCircle, AlertCircle, Send } from "lucide-react"
import { EmailQuery } from "@/lib/types"
import { formatDate } from "@/lib/utils"

interface RecentEmailsProps {
  emails: EmailQuery[]
}

export function RecentEmails({ emails }: RecentEmailsProps) {
  const getStatusIcon = (status: EmailQuery["responseStatus"]) => {
    switch (status) {
      case "sent":
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case "draft":
        return <Clock className="h-4 w-4 text-yellow-500" />
      case "failed":
        return <AlertCircle className="h-4 w-4 text-red-500" />
      default:
        return <Mail className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusBadge = (status: EmailQuery["responseStatus"]) => {
    const variants = {
      sent: "success" as const,
      draft: "warning" as const,
      failed: "destructive" as const,
    }
    return (
      <Badge variant={status === "sent" ? "secondary" : status === "draft" ? "outline" : "destructive"} className="capitalize">
        {status}
      </Badge>
    )
  }

  return (
    <Card className="col-span-3">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Mail className="h-5 w-5" />
          Recent Email Queries
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {emails.slice(0, 5).map((email) => (
            <div
              key={email.id}
              className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors"
            >
              <div className="flex items-start space-x-4 flex-1">
                {getStatusIcon(email.responseStatus)}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <p className="text-sm font-medium truncate">
                      {email.subject}
                    </p>
                    {getStatusBadge(email.responseStatus)}
                  </div>
                  <p className="text-xs text-muted-foreground mb-2">
                    From: {email.senderEmail}
                  </p>
                  <div className="text-xs text-muted-foreground">
                    {email.extractedInfo.checkIn && (
                      <span className="mr-4">
                        Check-in: {formatDate(email.extractedInfo.checkIn)}
                      </span>
                    )}
                    {email.extractedInfo.guests && (
                      <span className="mr-4">
                        Guests: {email.extractedInfo.guests}
                      </span>
                    )}
                    {email.extractedInfo.roomType && (
                      <span>
                        Room: {email.extractedInfo.roomType}
                      </span>
                    )}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground">
                  {formatDate(email.createdAt)}
                </span>
                {email.responseStatus === "draft" && (
                  <Button size="sm" variant="outline">
                    <Send className="h-3 w-3 mr-1" />
                    Send
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
        {emails.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            <Mail className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>No recent email queries</p>
            <p className="text-sm">Email responses will appear here</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
} 