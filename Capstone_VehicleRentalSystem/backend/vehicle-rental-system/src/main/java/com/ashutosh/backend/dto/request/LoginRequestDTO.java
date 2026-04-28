package com.ashutosh.backend.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Data Transfer Object for capturing user login credentials.
 * Transports authentication data from the client to the service layer
 * while enforcing format and presence checks.
 */
@Data
public class LoginRequestDTO {

    /**
     * The registered email address of the user.
     * Requires a non-blank value in a valid email format to pass initial validation.
     */
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    /**
     * The account password provided by the user.
     * Requires a non-blank value for authentication processing.
     */
    @NotBlank(message = "Password is required")
    private String password;
}