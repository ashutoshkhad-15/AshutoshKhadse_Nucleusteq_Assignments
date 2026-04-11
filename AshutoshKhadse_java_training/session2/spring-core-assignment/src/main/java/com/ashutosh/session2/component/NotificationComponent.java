package com.ashutosh.session2.component;

import org.springframework.stereotype.Component;

// used @Component so Spring knows to automatically create and manage this helper class for us
@Component
public class NotificationComponent {

    public String sendNotification(String recipient) {
        String message = "Hello, " + recipient + "! You have a new notification.";
        // printing it out to the console
        System.out.println("[NotificationComponent] Dispatching: " + message);
        return "Notification sent";
    }
}

