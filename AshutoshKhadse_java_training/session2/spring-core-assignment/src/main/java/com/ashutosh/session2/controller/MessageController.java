package com.ashutosh.session2.controller;

import com.ashutosh.session2.service.MessageService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

// This tells Spring that this class handles web requests and should automatically convert our responses into JSON format
@RestController
public class MessageController {

    private final MessageService messageService;

    // Using constructor injection so Spring automatically gives us the service when the app starts
    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }

    // Setting up our web endpoint. This method will run whenever someone goes to the "/message" URL using a GET request
    @GetMapping("/message")
    public ResponseEntity<Map<String, String>> getMessage(
            @RequestParam String type,
            @RequestParam(defaultValue = "Default message content") String payload) {

        String formatted = messageService.getFormattedMessage(type, payload);

        return ResponseEntity.ok(Map.of(
                "type",             type.toUpperCase(),
                "formattedMessage", formatted
        ));
    }
}

