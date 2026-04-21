package com.ashutosh.backend.enums;

// I created this enum to define different roles of users in the system
// I created this so that we avoid using hardcoded strings like "USER", "ADMIN" everywhere
public enum UserRole {

    // Default role for normal users of the application
    USER,
    // Role for admin users who will manage users, vehicles
    ADMIN
}
