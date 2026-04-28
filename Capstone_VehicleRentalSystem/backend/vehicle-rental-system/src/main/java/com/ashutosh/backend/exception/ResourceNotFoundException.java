package com.ashutosh.backend.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

/**
 * Custom exception triggered when a requested database entity (such as a User, Vehicle, or Booking)
 * cannot be located. Automatically maps to a 404 Not Found HTTP status.
 */
@ResponseStatus(HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException {

    /**
     * Constructs a new ResourceNotFoundException with the specified detail message.
     *
     * @param message The detail message explaining which resource could not be found.
     */
    public ResourceNotFoundException(String message) {
        super(message);
    }
}