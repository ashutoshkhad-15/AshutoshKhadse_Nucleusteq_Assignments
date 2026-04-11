package com.ashutosh.session2.service;

import com.ashutosh.session2.component.formatter.MessageFormatter;
import org.springframework.stereotype.Service;
import java.util.Map;

// Telling Spring this is a service class where we handle our main business logic
@Service
public class MessageService {

    // A map (like a dictionary) to hold all our different formatters.
    private final Map<String, MessageFormatter> formatterMap;

    // Constructor
    public MessageService(Map<String, MessageFormatter> formatterMap) {
        this.formatterMap = formatterMap;
    }

    // This method takes a message type and the actual text, then formats it properly
    public String getFormattedMessage(String type, String payload) {
        String normalizedType = type.toUpperCase();
        MessageFormatter formatter = formatterMap.get(normalizedType);

        if (formatter == null) {
            // Throwing a clear error so they know exactly what went wrong and what types are allowed
            throw new IllegalArgumentException(
                    "Unsupported message type: '" + type + "'. Supported types: SHORT, LONG"
            );
        }

        return formatter.format(payload);
    }
}
