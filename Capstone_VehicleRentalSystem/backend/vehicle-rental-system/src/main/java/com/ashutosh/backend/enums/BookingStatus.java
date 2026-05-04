package com.ashutosh.backend.enums;

/**
 * Represents the various stages of a vehicle rental lifecycle.
 * This enum is used to track the current state of a reservation and
 * trigger specific business logic, such as releasing a vehicle back
 * to the fleet or preventing duplicate bookings.
 */
public enum BookingStatus {

    /**
     * Indicates that the rental period has started and the vehicle is
     * currently with the user.
     */
    ACTIVE,

    /**
     * Indicates the booking is verified and the vehicle is reserved
     * for the upcoming trip.
     */
    CONFIRMED,

    /**
     * Indicates the reservation was voided by a user or an administrator
     * before the trip began.
     */
    CANCELLED,

    /**
     * Indicates the vehicle has been physically returned and the rental
     * transaction is closed.
     */
    COMPLETED
}