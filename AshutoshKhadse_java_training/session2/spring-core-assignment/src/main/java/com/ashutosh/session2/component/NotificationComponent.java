package com.ashutosh.session2.component;

import org.springframework.stereotype.Component;

@Component
public class NotificationComponent {

    public String sendNotification(String recipient) {
        String message = "Hello, " + recipient + "! You have a new notification.";
        System.out.println("[NotificationComponent] Dispatching: " + message);
        return "Notification sent";
    }
}

