package com.ashutosh.backend.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class RegisterRequestDTO {

    // this DTO grabs all the required fields from our AppUser database schema
    // so a new customer can successfully create an account.
    @NotBlank(message = "First name is required")
    @Size(min = 2, max = 50, message = "First name must be between 2 and 50 characters")
    @Pattern(regexp = "^[A-Za-z]+$", message = "First name must contain only letters")
    private String firstName;

    @NotBlank(message = "Last name is required")
    @Size(min = 2, max = 50, message = "Last name must be between 2 and 50 characters")
    @Pattern(regexp = "^[A-Za-z]+$", message = "Last name must contain only letters")
    private String lastName;

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    @Size(max = 100, message = "Email must not exceed 100 characters")
    private String email;

    // I added a @Size constraint to enforce basic password security rules
    // before the data even reaches our Service layer.
    @NotBlank(message = "Password is required")
    @Size(min = 6, message = "Password must be at least 6 characters long")
    private String password;

    @NotBlank(message = "Phone number is required")
    @Pattern(regexp = "^[0-9]{10}$", message = "Phone number must be exactly 10 digits")
    private String phoneNumber;

    // requiring this upfront satisfies my Capstone scope for real-world KYC logic.
    @NotBlank(message = "Driver's license number is required")
    @Size(min = 5, max = 20, message = "License number must be between 5 and 20 characters")
    @Pattern(
            regexp = "^[A-Z0-9]+$",
            message = "License must contain only uppercase letters and numbers"
    )
    private String driversLicenseNumber;
}