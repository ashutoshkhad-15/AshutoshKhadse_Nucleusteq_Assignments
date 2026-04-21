package com.ashutosh.backend.enums;

// This enum is used to represent the current status of a vehicle
// I created this to avoid using string values for status in different places
public enum VehicleStatus {

    // Vehicle is free and can be booked by users
    AVAILABLE,
    // Vehicle is currently booked by a user
    BOOKED,
    // Vehicle is under maintenance (not available for booking)
    MAINTENANCE,
    // Vehicle is no longer in use (maybe sold or removed from service)
    RETIRED
}
