"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { TrendingUp, TrendingDown } from "lucide-react"
import { LucideIcon } from "lucide-react"
import { useEffect, useState } from "react"

interface PremiumStatsCardProps {
  title: string
  value: string | number
  change: string
  changeType: "positive" | "negative" | "neutral"
  icon: LucideIcon
  description?: string
  progress?: number
  gradient?: string
}

export function PremiumStatsCard({
  title,
  value,
  change,
  changeType,
  icon: Icon,
  description,
  progress,
  gradient = "from-blue-500 to-blue-600"
}: PremiumStatsCardProps) {
  const [animatedValue, setAnimatedValue] = useState(0)
  const [isVisible, setIsVisible] = useState(false)

  // Animate number counting effect
  useEffect(() => {
    setIsVisible(true)
    const numericValue = typeof value === 'string' ? 
      parseInt(value.replace(/[^\d]/g, '')) || 0 : value
    
    let start = 0
    const end = numericValue
    const duration = 2000
    const increment = end / (duration / 16)

    const timer = setInterval(() => {
      start += increment
      if (start >= end) {
        setAnimatedValue(end)
        clearInterval(timer)
      } else {
        setAnimatedValue(Math.floor(start))
      }
    }, 16)

    return () => clearInterval(timer)
  }, [value])

  const formatValue = (val: number) => {
    if (typeof value === 'string' && value.includes('$')) {
      return `$${val.toLocaleString()}`
    }
    if (typeof value === 'string' && value.includes('%')) {
      return `${val}%`
    }
    if (typeof value === 'string' && value.includes('min')) {
      return `${val}min`
    }
    return val.toLocaleString()
  }

  const getChangeColor = () => {
    switch (changeType) {
      case "positive":
        return "text-emerald-600 bg-emerald-50 dark:text-emerald-400 dark:bg-emerald-900/20"
      case "negative":
        return "text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-900/20"
      default:
        return "text-gray-600 bg-gray-50 dark:text-gray-400 dark:bg-gray-800"
    }
  }

  const getTrendIcon = () => {
    if (changeType === "positive") return TrendingUp
    if (changeType === "negative") return TrendingDown
    return null
  }

  const TrendIcon = getTrendIcon()

  return (
    <Card className={`group relative overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300 ${isVisible ? 'animate-in slide-in-from-bottom-4' : ''}`}>
      {/* Gradient background */}
      <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-5 group-hover:opacity-10 transition-opacity duration-300`} />
      
      {/* Animated border gradient */}
      <div className={`absolute inset-0 bg-gradient-to-r ${gradient} opacity-20 blur-xl group-hover:opacity-30 transition-opacity duration-300`} />
      
      <CardContent className="relative p-6">
        <div className="flex items-center justify-between mb-4">
          <div className={`flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br ${gradient} shadow-lg`}>
            <Icon className="h-6 w-6 text-white" />
          </div>
          
          <Badge className={`${getChangeColor()} border-0 font-medium`}>
            {TrendIcon && <TrendIcon className="h-3 w-3 mr-1" />}
            {change}
          </Badge>
        </div>

        <div className="space-y-2">
          <h3 className="text-sm font-medium text-muted-foreground tracking-wide uppercase">
            {title}
          </h3>
          
          <div className="text-3xl font-bold text-foreground tracking-tight">
            {formatValue(animatedValue)}
          </div>
          
          {description && (
            <p className="text-xs text-muted-foreground">
              {description}
            </p>
          )}
          
          {progress !== undefined && (
            <div className="pt-2">
              <div className="flex items-center justify-between text-xs text-muted-foreground mb-1">
                <span>Progress</span>
                <span>{progress}%</span>
              </div>
              <Progress 
                value={progress} 
                className="h-2 bg-gray-100 dark:bg-gray-800"
              />
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
} 