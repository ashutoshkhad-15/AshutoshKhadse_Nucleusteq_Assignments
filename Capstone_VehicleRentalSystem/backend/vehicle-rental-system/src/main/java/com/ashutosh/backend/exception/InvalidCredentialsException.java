package com.ashutosh.backend.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

/**
 * Custom exception triggered during authentication failures, such as providing
 * an incorrect password or attempting to log into a deactivated account.
 * Automatically maps to a 401 Unauthorized HTTP status.
 */
@ResponseStatus(HttpStatus.UNAUTHORIZED)
public class InvalidCredentialsException extends RuntimeException {

    /**
     * Constructs a new InvalidCredentialsException with the specified detail message.
     *
     * @param message The detail message explaining the reason for the authentication failure.
     */
    public InvalidCredentialsException(String message) {
        super(message);
    }
}