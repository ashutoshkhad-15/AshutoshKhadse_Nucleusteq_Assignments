package com.ashutosh.session2.service;

import com.ashutosh.session2.component.NotificationComponent;
import org.springframework.stereotype.Service;

// Marking this as a Service so Spring knows it handles our business logic for notifications
@Service
public class NotificationService {

    private final NotificationComponent notificationComponent;
    // Constructor
    public NotificationService(NotificationComponent notificationComponent) {
        this.notificationComponent = notificationComponent;
    }
    // This is the main method we call when we want to trigger a message to someone
    public String triggerNotification(String recipient) {
        if (recipient == null || recipient.isBlank()) {
            // If the data is bad, stop right here and throw an error so we don't try to send a ghost message
            throw new IllegalArgumentException("Recipient must not be empty.");
        }
        return notificationComponent.sendNotification(recipient);
    }
}
