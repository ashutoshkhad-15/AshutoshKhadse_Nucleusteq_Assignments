package com.ashutosh.backend.enums;

/**
 * Represents the current operational state of a vehicle.
 * Used to determine if a vehicle can be shown in the catalog or reserved for a trip.
 */
public enum VehicleStatus {

    /**
     * Indicates the vehicle is free and ready for new user bookings.
     */
    AVAILABLE,

    /**
     * Indicates the vehicle is currently reserved for a confirmed or active trip.
     */
    BOOKED,

    /**
     * Indicates the vehicle is undergoing repairs and is temporarily unavailable.
     */
    MAINTENANCE,

    /**
     * Indicates the vehicle has been permanently removed from the active fleet.
     */
    RETIRED
}