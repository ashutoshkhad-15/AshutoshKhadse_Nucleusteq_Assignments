package com.ashutosh.backend.enums;

/**
 * Defines the types of fuel or energy sources used by the vehicles in the fleet.
 * Helps users filter vehicles based on their preferred engine technology and
 * provides technical details for each listing.
 */
public enum VehicleFuelType {

    /**
     * Standard gasoline-powered internal combustion engine.
     */
    PETROL,

    /**
     * Diesel-powered internal combustion engine.
     */
    DIESEL,

    /**
     * Fully electric vehicle powered by a battery.
     */
    EV,

    /**
     * Combined internal combustion engine and electric motor system.
     */
    HYBRID
}