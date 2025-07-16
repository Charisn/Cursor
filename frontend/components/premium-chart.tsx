"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
import { Area, AreaChart, ResponsiveContainer, XAxis, YAxis, CartesianGrid, Bar, BarChart, Line, LineChart } from "recharts"
import { CalendarDays, TrendingUp } from "lucide-react"

interface ChartDataPoint {
  name: string
  value: number
  secondary?: number
  date?: string
}

interface PremiumChartProps {
  title: string
  description?: string
  data: ChartDataPoint[]
  type?: "area" | "bar" | "line"
  gradient?: boolean
  height?: number
  showGrid?: boolean
  primaryColor?: string
  secondaryColor?: string
}

export function PremiumChart({
  title,
  description,
  data,
  type = "area",
  gradient = true,
  height = 300,
  showGrid = true,
  primaryColor = "#3b82f6",
  secondaryColor = "#10b981"
}: PremiumChartProps) {
  const chartConfig = {
    value: {
      label: "Primary",
      color: primaryColor,
    },
    secondary: {
      label: "Secondary", 
      color: secondaryColor,
    },
  } satisfies ChartConfig

  const renderChart = () => {
    switch (type) {
      case "bar":
        return (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="name" 
              axisLine={false}
              tickLine={false}
              className="text-xs text-muted-foreground"
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              className="text-xs text-muted-foreground"
            />
            <ChartTooltip content={<ChartTooltipContent />} />
            <Bar 
              dataKey="value" 
              fill={primaryColor}
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        )
      
      case "line":
        return (
          <LineChart data={data}>
            {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />}
            <XAxis 
              dataKey="name" 
              axisLine={false}
              tickLine={false}
              className="text-xs text-muted-foreground"
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              className="text-xs text-muted-foreground"
            />
            <ChartTooltip content={<ChartTooltipContent />} />
            <Line 
              type="monotone" 
              dataKey="value" 
              stroke={primaryColor}
              strokeWidth={3}
              dot={{ fill: primaryColor, strokeWidth: 2, r: 4 }}
            />
          </LineChart>
        )
      
      default: // area
        return (
          <AreaChart data={data}>
            {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />}
            <XAxis 
              dataKey="name" 
              axisLine={false}
              tickLine={false}
              className="text-xs text-muted-foreground"
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              className="text-xs text-muted-foreground"
            />
            <ChartTooltip content={<ChartTooltipContent />} />
            <defs>
              {gradient && (
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={primaryColor} stopOpacity={0.3}/>
                  <stop offset="95%" stopColor={primaryColor} stopOpacity={0}/>
                </linearGradient>
              )}
            </defs>
            <Area
              type="monotone"
              dataKey="value"
              stroke={primaryColor}
              fillOpacity={1}
              fill={gradient ? "url(#colorValue)" : primaryColor}
              strokeWidth={2}
            />
          </AreaChart>
        )
    }
  }

  // Calculate trend
  const firstValue = data[0]?.value || 0
  const lastValue = data[data.length - 1]?.value || 0
  const trend = lastValue > firstValue ? "up" : "down"
  const trendPercentage = firstValue > 0 ? Math.abs((lastValue - firstValue) / firstValue * 100) : 0

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="text-lg font-semibold">{title}</CardTitle>
            {description && (
              <CardDescription className="mt-1">{description}</CardDescription>
            )}
          </div>
          
          <div className="flex items-center gap-2 text-sm">
            <CalendarDays className="h-4 w-4 text-muted-foreground" />
            <span className="text-muted-foreground">Last 7 days</span>
          </div>
        </div>
        
        {/* Trend indicator */}
        <div className="flex items-center gap-2 mt-3">
          <TrendingUp className={`h-4 w-4 ${trend === 'up' ? 'text-emerald-600' : 'text-red-600'} ${trend === 'down' ? 'rotate-180' : ''}`} />
          <span className={`text-sm font-medium ${trend === 'up' ? 'text-emerald-600' : 'text-red-600'}`}>
            {trend === 'up' ? '+' : '-'}{trendPercentage.toFixed(1)}%
          </span>
          <span className="text-xs text-muted-foreground">vs last period</span>
        </div>
      </CardHeader>
      
      <CardContent className="pt-0">
        <ChartContainer config={chartConfig} className={`h-[${height}px] w-full`}>
          {renderChart()}
        </ChartContainer>
      </CardContent>
    </Card>
  )
} 