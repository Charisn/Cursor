import { z } from "zod"

// Base types
export interface Hotel {
  id: string
  name: string
  email: string
  address: string
  phone: string
  description: string
  amenities: string[]
  images: string[]
  rating: number
  createdAt: Date
  updatedAt: Date
}

export interface Room {
  id: string
  hotelId: string
  name: string
  type: string
  description: string
  capacity: number
  price: number
  currency: string
  amenities: string[]
  images: string[]
  isAvailable: boolean
}

export interface Booking {
  id: string
  hotelId: string
  roomId: string
  guestName: string
  guestEmail: string
  guestPhone: string
  checkInDate: Date
  checkOutDate: Date
  numberOfGuests: number
  totalPrice: number
  currency: string
  status: "pending" | "confirmed" | "cancelled" | "completed"
  createdAt: Date
  updatedAt: Date
}

export interface EmailQuery {
  id: string
  hotelId: string
  senderEmail: string
  subject: string
  content: string
  extractedInfo: {
    checkIn?: Date
    checkOut?: Date
    guests?: number
    roomType?: string
    specialRequests?: string[]
  }
  aiResponse: string
  responseStatus: "draft" | "sent" | "failed"
  createdAt: Date
}

// Zod schemas for validation
export const BookingRequestSchema = z.object({
  hotelId: z.string().min(1, "Hotel ID is required"),
  roomId: z.string().min(1, "Room ID is required"),
  guestName: z.string().min(2, "Guest name must be at least 2 characters"),
  guestEmail: z.string().email("Invalid email address"),
  guestPhone: z.string().min(10, "Phone number must be at least 10 digits"),
  checkInDate: z.string().refine((date) => new Date(date) > new Date(), {
    message: "Check-in date must be in the future",
  }),
  checkOutDate: z.string().refine((date) => new Date(date) > new Date(), {
    message: "Check-out date must be in the future",
  }),
  numberOfGuests: z.number().min(1, "Number of guests must be at least 1").max(10, "Maximum 10 guests allowed"),
})

export type BookingRequest = z.infer<typeof BookingRequestSchema>

// Dashboard stats
export interface DashboardStats {
  totalEmails: number
  emailsToday: number
  averageResponseTime: number
  bookingConversionRate: number
  totalRevenue: number
  activeBookings: number
} 