package com.ashutosh.session2.controller;

import com.ashutosh.session2.service.NotificationService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/notifications")
public class NotificationController {

    private final NotificationService notificationService;

    public NotificationController(NotificationService notificationService) {
        this.notificationService = notificationService;
    }

    @PostMapping("/trigger")
    public ResponseEntity<Map<String, String>> sendNotification(
            @RequestBody Map<String, String> requestBody) {

        if (!requestBody.containsKey("recipient") || requestBody.get("recipient").isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("error", "Recipient is required"));
        }

        String recipient = requestBody.get("recipient");
        String result = notificationService.triggerNotification(recipient);

        return ResponseEntity.ok(Map.of("message", result));
    }
}
