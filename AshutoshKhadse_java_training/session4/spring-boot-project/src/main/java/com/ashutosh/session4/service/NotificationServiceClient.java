package com.ashutosh.session4.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

// I annotated this class with @Service so that Spring's IoC container will automatically
// create an instance of it. This allows me to inject it directly into my TodoService
// using constructor injection
@Service
public class NotificationServiceClient {

    // I set up the SLF4J Logger here.
    // I made it 'private static final' because we only need one logger instance for the
    // entire class, and making it final prevents it from being modified accidentally.
    // Passing the class name (NotificationServiceClient.class) ensures the logs will
    // clearly show exactly where this message came from in the console.
    private static final Logger logger = LoggerFactory.getLogger(NotificationServiceClient.class);

    public void sendNotification(String message) {
        // I used the INFO level here because sending a notification is a standard,
        // successful business event (a "happy path").
        logger.info("Notification sent: {}", message);
    }
}