package com.ashutosh.backend.enums;

/**
 * Defines the different access levels for users in the system.
 * This enum is used to manage permissions and ensure users can only access
 * features appropriate for their specific role.
 */
public enum UserRole {

    /**
     * The default role for standard customers who use the platform to browse
     * and rent vehicles.
     */
    USER,

    /**
     * An elevated role for administrators who manage the vehicle fleet,
     * system bookings, and user accounts.
     */
    ADMIN
}