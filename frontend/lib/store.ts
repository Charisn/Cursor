import { create } from "zustand"
import { DashboardStats, Hotel, Room, Booking, EmailQuery } from "./types"

interface AppState {
  // Dashboard data
  stats: DashboardStats | null
  hotels: Hotel[]
  rooms: Room[]
  bookings: Booking[]
  emailQueries: EmailQuery[]
  
  // UI state
  isLoading: boolean
  error: string | null
  
  // Actions
  setStats: (stats: DashboardStats) => void
  setHotels: (hotels: Hotel[]) => void
  setRooms: (rooms: Room[]) => void
  setBookings: (bookings: Booking[]) => void
  setEmailQueries: (queries: EmailQuery[]) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  addBooking: (booking: Booking) => void
  updateBookingStatus: (bookingId: string, status: Booking["status"]) => void
}

export const useAppStore = create<AppState>((set, get) => ({
  // Initial state
  stats: null,
  hotels: [],
  rooms: [],
  bookings: [],
  emailQueries: [],
  isLoading: false,
  error: null,
  
  // Actions
  setStats: (stats) => set({ stats }),
  setHotels: (hotels) => set({ hotels }),
  setRooms: (rooms) => set({ rooms }),
  setBookings: (bookings) => set({ bookings }),
  setEmailQueries: (emailQueries) => set({ emailQueries }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  
  addBooking: (booking) => 
    set((state) => ({ bookings: [...state.bookings, booking] })),
  
  updateBookingStatus: (bookingId, status) =>
    set((state) => ({
      bookings: state.bookings.map((booking) =>
        booking.id === bookingId ? { ...booking, status } : booking
      ),
    })),
}))

// Mock data for development
export const mockStats: DashboardStats = {
  totalEmails: 1247,
  emailsToday: 23,
  averageResponseTime: 2.3,
  bookingConversionRate: 34.5,
  totalRevenue: 125420,
  activeBookings: 87,
}

export const mockHotels: Hotel[] = [
  {
    id: "hotel-1",
    name: "Grand Plaza Hotel",
    email: "reservations@grandplaza.com",
    address: "123 Main St, New York, NY 10001",
    phone: "+1 (555) 123-4567",
    description: "Luxury hotel in the heart of Manhattan",
    amenities: ["WiFi", "Pool", "Gym", "Spa", "Restaurant", "Bar"],
    images: ["/api/placeholder/400/300"],
    rating: 4.5,
    createdAt: new Date("2024-01-01"),
    updatedAt: new Date("2024-07-15"),
  },
]

export const mockRooms: Room[] = [
  {
    id: "room-1",
    hotelId: "hotel-1",
    name: "Deluxe King Room",
    type: "Deluxe",
    description: "Spacious room with king bed and city views",
    capacity: 2,
    price: 299,
    currency: "USD",
    amenities: ["King Bed", "City View", "Mini Bar", "WiFi"],
    images: ["/api/placeholder/400/300"],
    isAvailable: true,
  },
  {
    id: "room-2",
    hotelId: "hotel-1",
    name: "Executive Suite",
    type: "Suite",
    description: "Luxury suite with separate living area",
    capacity: 4,
    price: 599,
    currency: "USD",
    amenities: ["King Bed", "Living Area", "Kitchen", "Balcony"],
    images: ["/api/placeholder/400/300"],
    isAvailable: true,
  },
] 