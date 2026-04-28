package com.ashutosh.backend.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

/**
 * Custom exception triggered when a user attempts to create a record that violates
 * a unique constraint in the database, such as registering an email or license plate
 * that already exists. Automatically maps to a 409 Conflict HTTP status.
 */
@ResponseStatus(HttpStatus.CONFLICT)
public class DuplicateResourceException extends RuntimeException {

    /**
     * Constructs a new DuplicateResourceException with the specified detail message.
     *
     * @param message The detail message explaining which resource caused the conflict.
     */
    public DuplicateResourceException(String message) {
        super(message);
    }
}