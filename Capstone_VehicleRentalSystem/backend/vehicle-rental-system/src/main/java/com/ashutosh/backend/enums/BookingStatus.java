package com.ashutosh.backend.enums;

// This enum is used to track the status of a booking
// I created this as it also helps in applying business rules based on status easily
public enum BookingStatus {

    // Booking is created but not yet confirmed (waiting for approval)
    PENDING,
    // Booking is confirmed and vehicle is reserved for the user
    CONFIRMED,
    // Booking is cancelled by user or admin
    CANCELLED,
    // Booking is completed after the vehicle has been returned
    COMPLETED
}
