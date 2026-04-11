package com.ashutosh.session2.controller;

import com.ashutosh.session2.service.MessageService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
public class MessageController {

    private final MessageService messageService;

    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }

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

