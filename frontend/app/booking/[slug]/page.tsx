"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { 
  Calendar,
  Users,
  MapPin,
  Star,
  Wifi,
  Car,
  Coffee,
  ArrowLeft,
  CreditCard,
  Shield,
  CheckCircle
} from "lucide-react"
import { Room, Hotel, BookingRequest } from "@/lib/types"
import { formatCurrency, formatDate } from "@/lib/utils"
import { useAppStore, mockRooms, mockHotels } from "@/lib/store"

export default function BookingPage() {
  const params = useParams()
  const slug = params.slug as string
  const [selectedRoom, setSelectedRoom] = useState<Room | null>(null)
  const [hotel, setHotel] = useState<Hotel | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [bookingStep, setBookingStep] = useState<'details' | 'payment' | 'confirmation'>('details')
  const [guestInfo, setGuestInfo] = useState({
    name: '',
    email: '',
    phone: '',
    checkIn: '',
    checkOut: '',
    guests: 1,
    specialRequests: ''
  })

  const { addBooking } = useAppStore()

  useEffect(() => {
    // Simulate fetching booking data based on slug
    // In real implementation, this would be an API call
    const fetchBookingData = async () => {
      setIsLoading(true)
      
      // Mock API call delay
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Find room and hotel based on slug
      let room = mockRooms.find(r => r.id === 'room-1') // Default to first room
      
      // Handle specific booking scenarios based on slug
      if (slug === 'grand-plaza-deluxe-december') {
        room = mockRooms.find(r => r.name === 'Deluxe King Room') || mockRooms[0]
      } else if (slug === 'grand-plaza-suite-weekend') {
        room = mockRooms.find(r => r.name === 'Executive Suite') || mockRooms[1]
      }
      
      const hotelData = mockHotels.find(h => h.id === room?.hotelId)
      
      if (room && hotelData) {
        setSelectedRoom(room)
        setHotel(hotelData)
        
        // Pre-fill some booking data based on the booking scenario
        if (slug === 'grand-plaza-deluxe-december') {
          setGuestInfo(prev => ({
            ...prev,
            checkIn: '2024-12-15',
            checkOut: '2024-12-18',
            guests: 2,
            name: 'John Doe',
            email: 'john.doe@email.com'
          }))
        } else if (slug === 'grand-plaza-suite-weekend') {
          setGuestInfo(prev => ({
            ...prev,
            checkIn: '2024-11-16',
            checkOut: '2024-11-18',
            guests: 4,
            name: 'Sarah Wilson',
            email: 'sarah.wilson@company.com'
          }))
        } else {
          // Default booking data
          setGuestInfo(prev => ({
            ...prev,
            checkIn: '2024-12-15',
            checkOut: '2024-12-18',
            guests: 2
          }))
        }
      }
      
      setIsLoading(false)
    }

    fetchBookingData()
  }, [slug])

  const calculateNights = () => {
    if (!guestInfo.checkIn || !guestInfo.checkOut) return 0
    const checkIn = new Date(guestInfo.checkIn)
    const checkOut = new Date(guestInfo.checkOut)
    return Math.ceil((checkOut.getTime() - checkIn.getTime()) / (1000 * 60 * 60 * 24))
  }

  const calculateTotal = () => {
    if (!selectedRoom) return 0
    const nights = calculateNights()
    return selectedRoom.price * nights
  }

  const handleBookingSubmit = async () => {
    if (!selectedRoom || !hotel) return

    const newBooking = {
      id: `booking-${Date.now()}`,
      hotelId: hotel.id,
      roomId: selectedRoom.id,
      guestName: guestInfo.name,
      guestEmail: guestInfo.email,
      guestPhone: guestInfo.phone,
      checkInDate: new Date(guestInfo.checkIn),
      checkOutDate: new Date(guestInfo.checkOut),
      numberOfGuests: guestInfo.guests,
      totalPrice: calculateTotal(),
      currency: selectedRoom.currency,
      status: "confirmed" as const,
      createdAt: new Date(),
      updatedAt: new Date(),
    }

    // Add booking to store
    addBooking(newBooking)
    setBookingStep('confirmation')
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading booking details...</p>
        </div>
      </div>
    )
  }

  if (!selectedRoom || !hotel) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="pt-6 text-center">
            <h2 className="text-xl font-semibold mb-2">Booking Not Found</h2>
            <p className="text-muted-foreground mb-4">
              The booking link you're looking for doesn't exist or has expired.
            </p>
            <Button onClick={() => window.history.back()}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Go Back
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b sticky top-0 z-40">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button 
                variant="ghost" 
                onClick={() => window.history.back()}
                className="flex items-center gap-2"
              >
                <ArrowLeft className="h-4 w-4" />
                Back
              </Button>
              <div>
                <h1 className="text-xl font-semibold">{hotel.name}</h1>
                <p className="text-sm text-muted-foreground flex items-center gap-1">
                  <MapPin className="h-3 w-3" />
                  {hotel.address}
                </p>
              </div>
            </div>
            <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100">
              Secure Booking
            </Badge>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column - Booking Form */}
          <div className="lg:col-span-2 space-y-6">
            {bookingStep === 'details' && (
              <Card>
                <CardHeader>
                  <CardTitle>Guest Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Full Name *</label>
                      <input
                        type="text"
                        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        value={guestInfo.name}
                        onChange={(e) => setGuestInfo(prev => ({ ...prev, name: e.target.value }))}
                        placeholder="Enter your full name"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Email Address *</label>
                      <input
                        type="email"
                        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        value={guestInfo.email}
                        onChange={(e) => setGuestInfo(prev => ({ ...prev, email: e.target.value }))}
                        placeholder="Enter your email"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Phone Number *</label>
                      <input
                        type="tel"
                        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        value={guestInfo.phone}
                        onChange={(e) => setGuestInfo(prev => ({ ...prev, phone: e.target.value }))}
                        placeholder="Enter your phone number"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Number of Guests</label>
                      <select
                        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        value={guestInfo.guests}
                        onChange={(e) => setGuestInfo(prev => ({ ...prev, guests: parseInt(e.target.value) }))}
                      >
                        {[1, 2, 3, 4].map(num => (
                          <option key={num} value={num}>{num} Guest{num > 1 ? 's' : ''}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Check-in Date</label>
                      <input
                        type="date"
                        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        value={guestInfo.checkIn}
                        onChange={(e) => setGuestInfo(prev => ({ ...prev, checkIn: e.target.value }))}
                        min={new Date().toISOString().split('T')[0]}
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Check-out Date</label>
                      <input
                        type="date"
                        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        value={guestInfo.checkOut}
                        onChange={(e) => setGuestInfo(prev => ({ ...prev, checkOut: e.target.value }))}
                        min={guestInfo.checkIn || new Date().toISOString().split('T')[0]}
                        required
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Special Requests</label>
                    <textarea
                      className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      rows={3}
                      value={guestInfo.specialRequests}
                      onChange={(e) => setGuestInfo(prev => ({ ...prev, specialRequests: e.target.value }))}
                      placeholder="Any special requests or preferences..."
                    />
                  </div>
                  
                  <Button 
                    className="w-full"
                    onClick={() => setBookingStep('payment')}
                    disabled={!guestInfo.name || !guestInfo.email || !guestInfo.phone || !guestInfo.checkIn || !guestInfo.checkOut}
                  >
                    Continue to Payment
                    <CreditCard className="h-4 w-4 ml-2" />
                  </Button>
                </CardContent>
              </Card>
            )}

            {bookingStep === 'payment' && (
              <Card>
                <CardHeader>
                  <CardTitle>Payment Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Shield className="h-5 w-5 text-blue-600" />
                      <h3 className="font-medium">Secure Payment</h3>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Your payment information is encrypted and secure. We use industry-standard security measures.
                    </p>
                  </div>
                  
                  <div className="grid gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Card Number</label>
                      <input
                        type="text"
                        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="1234 5678 9012 3456"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium mb-1">Expiry Date</label>
                        <input
                          type="text"
                          className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="MM/YY"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-1">CVV</label>
                        <input
                          type="text"
                          className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="123"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Cardholder Name</label>
                      <input
                        type="text"
                        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter cardholder name"
                      />
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <Button 
                      variant="outline" 
                      onClick={() => setBookingStep('details')}
                      className="flex-1"
                    >
                      Back
                    </Button>
                    <Button 
                      onClick={handleBookingSubmit}
                      className="flex-1 bg-green-600 hover:bg-green-700"
                    >
                      Complete Booking
                      <CheckCircle className="h-4 w-4 ml-2" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {bookingStep === 'confirmation' && (
              <Card className="border-green-200 dark:border-green-800">
                <CardContent className="pt-6 text-center">
                  <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-4" />
                  <h2 className="text-2xl font-bold text-green-700 dark:text-green-400 mb-2">
                    Booking Confirmed!
                  </h2>
                  <p className="text-muted-foreground mb-6">
                    Your reservation has been confirmed. A confirmation email will be sent to {guestInfo.email}
                  </p>
                  <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg mb-6">
                    <h3 className="font-semibold mb-2">Booking Details</h3>
                    <div className="text-sm space-y-1">
                      <p><strong>Guest:</strong> {guestInfo.name}</p>
                      <p><strong>Hotel:</strong> {hotel.name}</p>
                      <p><strong>Room:</strong> {selectedRoom.name}</p>
                      <p><strong>Check-in:</strong> {formatDate(guestInfo.checkIn)}</p>
                      <p><strong>Check-out:</strong> {formatDate(guestInfo.checkOut)}</p>
                      <p><strong>Total Paid:</strong> {formatCurrency(calculateTotal())}</p>
                    </div>
                  </div>
                  <Button onClick={() => window.location.href = '/'}>
                    Return to Dashboard
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column - Booking Summary */}
          <div className="space-y-6">
            <Card className="sticky top-24">
              <CardHeader>
                <CardTitle>Booking Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Room Details */}
                <div className="border-b pb-4">
                  <h3 className="font-semibold text-lg mb-2">{selectedRoom.name}</h3>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground mb-2">
                    <span className="flex items-center gap-1">
                      <Users className="h-3 w-3" />
                      Up to {selectedRoom.capacity} guests
                    </span>
                    <span className="flex items-center gap-1">
                      <Star className="h-3 w-3 fill-current text-yellow-500" />
                      {hotel.rating}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground mb-3">{selectedRoom.description}</p>
                  
                  {/* Amenities */}
                  <div className="flex flex-wrap gap-2">
                    {selectedRoom.amenities.slice(0, 3).map((amenity, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {amenity}
                      </Badge>
                    ))}
                    {selectedRoom.amenities.length > 3 && (
                      <Badge variant="secondary" className="text-xs">
                        +{selectedRoom.amenities.length - 3} more
                      </Badge>
                    )}
                  </div>
                </div>

                {/* Pricing Breakdown */}
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm">Room rate per night</span>
                    <span className="text-sm">{formatCurrency(selectedRoom.price)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Number of nights</span>
                    <span className="text-sm">{calculateNights()}</span>
                  </div>
                  <div className="border-t pt-2 flex justify-between font-semibold">
                    <span>Total</span>
                    <span>{formatCurrency(calculateTotal())}</span>
                  </div>
                </div>

                {/* Stay Details */}
                {guestInfo.checkIn && guestInfo.checkOut && (
                  <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Calendar className="h-4 w-4" />
                      <span className="font-medium text-sm">Your Stay</span>
                    </div>
                    <div className="text-sm space-y-1">
                      <p><strong>Check-in:</strong> {formatDate(guestInfo.checkIn)}</p>
                      <p><strong>Check-out:</strong> {formatDate(guestInfo.checkOut)}</p>
                      <p><strong>Guests:</strong> {guestInfo.guests}</p>
                    </div>
                  </div>
                )}

                {/* Hotel Contact */}
                <div className="border-t pt-4">
                  <h4 className="font-medium mb-2">Hotel Contact</h4>
                  <div className="text-sm space-y-1 text-muted-foreground">
                    <p>{hotel.phone}</p>
                    <p>{hotel.email}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
} 