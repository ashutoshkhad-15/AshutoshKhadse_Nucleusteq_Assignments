package com.ashutosh.backend.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * Data Transfer Object for capturing user registration details.
 * Collects and validates all necessary personal and licensing information
 * before an account is created in the system.
 */
@Data
public class RegisterRequestDTO {

    /**
     * The user's first name. Enforces alphabetic characters and length
     * constraints to ensure data quality and consistency.
     */
    @NotBlank(message = "First name is required")
    @Size(min = 2, max = 50, message = "First name must be between 2 and 50 characters")
    @Pattern(regexp = "^[A-Za-z]+$", message = "First name must contain only letters")
    private String firstName;

    /**
     * The user's last name. Requires letters only and specific length
     * limits to match standard identity records.
     */
    @NotBlank(message = "Last name is required")
    @Size(min = 2, max = 50, message = "Last name must be between 2 and 50 characters")
    @Pattern(regexp = "^[A-Za-z]+$", message = "Last name must contain only letters")
    private String lastName;

    /**
     * The primary email for the account. Validates the format and domain
     * to ensure the address is reachable and serves as a valid login ID.
     */
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    @Pattern(
            regexp = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$",
            message = "Email must contain a valid domain like .com"
    )
    @Size(max = 100, message = "Email must not exceed 100 characters")
    private String email;

    /**
     * The account password. Enforces a minimum length of 6 characters
     * as a basic security measure before the value is hashed.
     */
    @NotBlank(message = "Password is required")
    @Size(min = 6, message = "Password must be at least 6 characters long")
    private String password;

    /**
     * The 10-digit mobile number. Enforces a strict numeric pattern
     * to maintain uniform contact records.
     */
    @NotBlank(message = "Phone number is required")
    @Pattern(regexp = "^[0-9]{10}$", message = "Phone number must be exactly 10 digits")
    private String phoneNumber;

    /**
     * The legal driver's license identifier. Validates the format and
     * length to ensure the user is eligible for vehicle rentals.
     */
    @NotBlank(message = "Driver's license number is required")
    @Size(min = 5, max = 20, message = "License number must be between 5 and 20 characters")
    @Pattern(
            regexp = "^[A-Z0-9]+$",
            message = "License must contain only uppercase letters and numbers"
    )
    private String driversLicenseNumber;
}