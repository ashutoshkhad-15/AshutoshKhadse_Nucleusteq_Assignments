package com.ashutosh.session2.controller;

import com.ashutosh.session2.service.NotificationService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
// Telling Spring this class handles web requests
@RestController
// @RequestMapping means all URLs in this controller will start with "/notifications"
@RequestMapping("/notifications")
public class NotificationController {

    private final NotificationService notificationService;

    // Constructor injection
    public NotificationController(NotificationService notificationService) {
        this.notificationService = notificationService;
    }

    // @PostMapping means this method runs when someone sends a POST request to "/notifications/trigger"
    @PostMapping("/trigger")
    public ResponseEntity<Map<String, String>> sendNotification(
            // @RequestBody grabs the JSON data the user sent and turns it into a Java Map so we can read it
            @RequestBody Map<String, String> requestBody) {

        // If they forgot it, or left it blank, we stop right here and send back a 400 Bad Request error
        if (!requestBody.containsKey("recipient") || requestBody.get("recipient").isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("error", "Recipient is required"));
        }

        String recipient = requestBody.get("recipient");
        String result = notificationService.triggerNotification(recipient);

        return ResponseEntity.ok(Map.of("message", result));
    }
}
