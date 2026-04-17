package com.ashutosh.session4.exception;

import com.ashutosh.session4.entity.TodoStatus;
// I created this custom exception to show that
// Tasks can only transition from PENDING to COMPLETED or COMPLETED to PENDING
// Instead of just returning a generic "Bad Request", displaying a clear message
public class InvalidStatusTransitionException extends RuntimeException {

    // I'm storing the exact transition the user attempted.
    // Keeping these 'final' ensures the details of the error can't be accidentally changed later.
    private final TodoStatus fromStatus;
    private final TodoStatus toStatus;

    public InvalidStatusTransitionException(TodoStatus fromStatus, TodoStatus toStatus) {
        // I added a detailed message in super
        super("Invalid status transition from " + fromStatus + " to " + toStatus +
                ". Allowed transitions: PENDING ↔ COMPLETED");
        this.fromStatus = fromStatus;
        this.toStatus = toStatus;
    }

    // I added these getters so that our Global Exception Handler can actually pull out exact data

    public TodoStatus getFromStatus() {
        return fromStatus;
    }

    public TodoStatus getToStatus() {
        return toStatus;
    }
}