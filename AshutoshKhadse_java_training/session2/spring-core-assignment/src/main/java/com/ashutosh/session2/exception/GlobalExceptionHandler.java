package com.ashutosh.session2.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.HashMap;
import java.util.Map;

// If any of our controllers throw an error, it gets caught here instead of breaking the app.
@RestControllerAdvice
public class GlobalExceptionHandler {

    // This method handles general runtime errors
    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, String>> handleRunTimeException(RuntimeException ex) {
        // Making a map so our error message gets converted into a clean JSON response
        Map<String, String> error = new HashMap<>();
        error.put("error", ex.getMessage());
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }

    // This method catches errors where bad data or wrong arguments were given
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<Map<String, String>> handleIllegalArgumentException(IllegalArgumentException ex) {
        // Packing the error message into a map just like above
        Map<String, String> error = new HashMap<>();
        error.put("error", ex.getMessage());
        return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
    }
}

